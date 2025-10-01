"""
WebSocket Server for Real-time Auction Updates in Mzadd Platform
Handles live bidding, notifications, and auction status updates
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional
import jwt
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from models_enhanced import db, User, Auction, Bid, AuctionStatus
from business_logic import revenue_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuctionWebSocketServer:
    """Manages WebSocket connections and real-time auction updates"""
    
    def __init__(self, app: Flask, secret_key: str):
        self.app = app
        self.secret_key = secret_key
        self.socketio = SocketIO(
            app, 
            cors_allowed_origins="*",
            async_mode='threading',
            logger=True,
            engineio_logger=True
        )
        
        # Connection tracking
        self.connected_users: Dict[str, Dict] = {}  # session_id -> user_info
        self.auction_participants: Dict[int, Set[str]] = {}  # auction_id -> set of session_ids
        self.user_sessions: Dict[int, Set[str]] = {}  # user_id -> set of session_ids
        
        # Auction timers
        self.auction_timers: Dict[int, asyncio.Task] = {}
        
        self.setup_event_handlers()
    
    def setup_event_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect(auth=None):
            """Handle client connection"""
            session_id = self.socketio.request.sid
            logger.info(f"Client connected: {session_id}")
            
            # Send connection confirmation
            emit('connection_status', {
                'status': 'connected',
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            session_id = self.socketio.request.sid
            logger.info(f"Client disconnected: {session_id}")
            
            # Clean up user session
            if session_id in self.connected_users:
                user_info = self.connected_users[session_id]
                user_id = user_info.get('user_id')
                
                # Remove from user sessions
                if user_id and user_id in self.user_sessions:
                    self.user_sessions[user_id].discard(session_id)
                    if not self.user_sessions[user_id]:
                        del self.user_sessions[user_id]
                
                # Remove from auction rooms
                for auction_id, participants in self.auction_participants.items():
                    participants.discard(session_id)
                
                del self.connected_users[session_id]
        
        @self.socketio.on('authenticate')
        def handle_authenticate(data):
            """Handle user authentication"""
            session_id = self.socketio.request.sid
            token = data.get('token')
            
            if not token:
                emit('auth_error', {'message': 'Token required'})
                return
            
            try:
                # Decode JWT token
                payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
                user_id = payload.get('user_id')
                
                if not user_id:
                    emit('auth_error', {'message': 'Invalid token'})
                    return
                
                # Get user from database
                user = User.query.get(user_id)
                if not user or not user.is_active:
                    emit('auth_error', {'message': 'User not found or inactive'})
                    return
                
                # Store user session
                self.connected_users[session_id] = {
                    'user_id': user_id,
                    'username': user.username,
                    'role': user.role.value,
                    'connected_at': datetime.utcnow()
                }
                
                # Track user sessions
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = set()
                self.user_sessions[user_id].add(session_id)
                
                logger.info(f"User authenticated: {user.username} ({session_id})")
                
                emit('auth_success', {
                    'user_id': user_id,
                    'username': user.username,
                    'role': user.role.value
                })
                
            except jwt.ExpiredSignatureError:
                emit('auth_error', {'message': 'Token expired'})
            except jwt.InvalidTokenError:
                emit('auth_error', {'message': 'Invalid token'})
            except Exception as e:
                logger.error(f"Authentication error: {str(e)}")
                emit('auth_error', {'message': 'Authentication failed'})
        
        @self.socketio.on('join_auction')
        def handle_join_auction(data):
            """Handle user joining an auction room"""
            session_id = self.socketio.request.sid
            auction_id = data.get('auction_id')
            
            if session_id not in self.connected_users:
                emit('error', {'message': 'Not authenticated'})
                return
            
            if not auction_id:
                emit('error', {'message': 'Auction ID required'})
                return
            
            try:
                # Verify auction exists and is active
                auction = Auction.query.get(auction_id)
                if not auction:
                    emit('error', {'message': 'Auction not found'})
                    return
                
                # Join auction room
                join_room(f'auction_{auction_id}')
                
                # Track participant
                if auction_id not in self.auction_participants:
                    self.auction_participants[auction_id] = set()
                self.auction_participants[auction_id].add(session_id)
                
                user_info = self.connected_users[session_id]
                logger.info(f"User {user_info['username']} joined auction {auction_id}")
                
                # Send current auction state
                emit('auction_joined', {
                    'auction_id': auction_id,
                    'auction_data': auction.to_dict(include_item=True),
                    'participants_count': len(self.auction_participants[auction_id])
                })
                
                # Notify other participants
                emit('participant_joined', {
                    'username': user_info['username'],
                    'participants_count': len(self.auction_participants[auction_id])
                }, room=f'auction_{auction_id}', include_self=False)
                
            except Exception as e:
                logger.error(f"Error joining auction: {str(e)}")
                emit('error', {'message': 'Failed to join auction'})
        
        @self.socketio.on('leave_auction')
        def handle_leave_auction(data):
            """Handle user leaving an auction room"""
            session_id = self.socketio.request.sid
            auction_id = data.get('auction_id')
            
            if session_id not in self.connected_users:
                return
            
            if auction_id and auction_id in self.auction_participants:
                self.auction_participants[auction_id].discard(session_id)
                leave_room(f'auction_{auction_id}')
                
                user_info = self.connected_users[session_id]
                logger.info(f"User {user_info['username']} left auction {auction_id}")
                
                # Notify other participants
                emit('participant_left', {
                    'username': user_info['username'],
                    'participants_count': len(self.auction_participants[auction_id])
                }, room=f'auction_{auction_id}')
        
        @self.socketio.on('place_bid')
        def handle_place_bid(data):
            """Handle bid placement"""
            session_id = self.socketio.request.sid
            
            if session_id not in self.connected_users:
                emit('bid_error', {'message': 'Not authenticated'})
                return
            
            user_info = self.connected_users[session_id]
            user_id = user_info['user_id']
            auction_id = data.get('auction_id')
            bid_amount = data.get('amount')
            
            if not auction_id or not bid_amount:
                emit('bid_error', {'message': 'Auction ID and bid amount required'})
                return
            
            try:
                # Validate bid
                validation_result = self.validate_bid(user_id, auction_id, bid_amount)
                if not validation_result['valid']:
                    emit('bid_error', {'message': validation_result['message']})
                    return
                
                # Create bid
                bid = Bid(
                    auction_id=auction_id,
                    bidder_id=user_id,
                    amount=float(bid_amount),
                    timestamp=datetime.utcnow(),
                    is_valid=True
                )
                
                db.session.add(bid)
                
                # Update auction
                auction = Auction.query.get(auction_id)
                auction.current_price = float(bid_amount)
                auction.winning_bid_id = bid.id
                auction.total_bids += 1
                
                # Update unique bidders count
                existing_bidder = Bid.query.filter_by(
                    auction_id=auction_id, 
                    bidder_id=user_id
                ).first()
                if not existing_bidder:
                    auction.unique_bidders += 1
                
                db.session.commit()
                
                logger.info(f"Bid placed: {bid_amount} KWD by {user_info['username']} on auction {auction_id}")
                
                # Broadcast bid to all auction participants
                bid_data = {
                    'auction_id': auction_id,
                    'bid_id': bid.id,
                    'amount': float(bid_amount),
                    'bidder_name': user_info['username'],
                    'timestamp': bid.timestamp.isoformat(),
                    'total_bids': auction.total_bids,
                    'unique_bidders': auction.unique_bidders
                }
                
                emit('new_bid', bid_data, room=f'auction_{auction_id}')
                
                # Send confirmation to bidder
                emit('bid_confirmation', {
                    'success': True,
                    'bid_id': bid.id,
                    'amount': float(bid_amount),
                    'auction_id': auction_id
                })
                
                # Check if auction should be extended (last 5 minutes)
                time_remaining = (auction.end_time - datetime.utcnow()).total_seconds()
                if time_remaining < 300:  # 5 minutes
                    auction.extend_auction(300)  # Extend by 5 minutes
                    db.session.commit()
                    
                    emit('auction_extended', {
                        'auction_id': auction_id,
                        'new_end_time': auction.end_time.isoformat(),
                        'extension_time': 300
                    }, room=f'auction_{auction_id}')
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error placing bid: {str(e)}")
                emit('bid_error', {'message': 'Failed to place bid'})
        
        @self.socketio.on('get_auction_status')
        def handle_get_auction_status(data):
            """Handle auction status request"""
            auction_id = data.get('auction_id')
            
            if not auction_id:
                emit('error', {'message': 'Auction ID required'})
                return
            
            try:
                auction = Auction.query.get(auction_id)
                if not auction:
                    emit('error', {'message': 'Auction not found'})
                    return
                
                emit('auction_status', {
                    'auction_id': auction_id,
                    'auction_data': auction.to_dict(include_item=True, include_bids=True)
                })
                
            except Exception as e:
                logger.error(f"Error getting auction status: {str(e)}")
                emit('error', {'message': 'Failed to get auction status'})
    
    def validate_bid(self, user_id: int, auction_id: int, bid_amount: float) -> Dict:
        """Validate bid before processing"""
        try:
            # Get auction
            auction = Auction.query.get(auction_id)
            if not auction:
                return {'valid': False, 'message': 'Auction not found'}
            
            # Check auction status
            if auction.status != AuctionStatus.ACTIVE:
                return {'valid': False, 'message': 'Auction is not active'}
            
            # Check if auction has ended
            if datetime.utcnow() > auction.end_time:
                return {'valid': False, 'message': 'Auction has ended'}
            
            # Check if user is the item owner
            if auction.item.owner_id == user_id:
                return {'valid': False, 'message': 'Cannot bid on your own item'}
            
            # Check minimum bid increment (5 KWD)
            min_bid = auction.current_price + 5
            if bid_amount < min_bid:
                return {'valid': False, 'message': f'Minimum bid is {min_bid} KWD'}
            
            # Check if user has sufficient balance (simplified check)
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return {'valid': False, 'message': 'User not found or inactive'}
            
            return {'valid': True}
            
        except Exception as e:
            logger.error(f"Error validating bid: {str(e)}")
            return {'valid': False, 'message': 'Validation failed'}
    
    def broadcast_auction_update(self, auction_id: int, update_data: Dict):
        """Broadcast auction update to all participants"""
        self.socketio.emit('auction_update', {
            'auction_id': auction_id,
            'update_data': update_data,
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'auction_{auction_id}')
    
    def broadcast_auction_ended(self, auction_id: int):
        """Broadcast auction end notification"""
        try:
            auction = Auction.query.get(auction_id)
            if not auction:
                return
            
            # Update auction status
            auction.status = AuctionStatus.CLOSED
            
            # Process revenue if there's a winner
            if auction.winning_bid_id:
                revenue_result = revenue_manager.process_auction_completion(auction_id)
                logger.info(f"Revenue processed for auction {auction_id}: {revenue_result}")
            
            db.session.commit()
            
            # Broadcast to all participants
            self.socketio.emit('auction_ended', {
                'auction_id': auction_id,
                'final_price': auction.current_price,
                'winner_id': auction.winning_bid.bidder_id if auction.winning_bid else None,
                'total_bids': auction.total_bids,
                'timestamp': datetime.utcnow().isoformat()
            }, room=f'auction_{auction_id}')
            
            logger.info(f"Auction {auction_id} ended - Final price: {auction.current_price} KWD")
            
        except Exception as e:
            logger.error(f"Error ending auction {auction_id}: {str(e)}")
    
    def send_notification_to_user(self, user_id: int, notification_data: Dict):
        """Send notification to specific user"""
        if user_id in self.user_sessions:
            for session_id in self.user_sessions[user_id]:
                self.socketio.emit('notification', notification_data, room=session_id)
    
    def get_active_auctions_count(self) -> int:
        """Get count of active auctions with participants"""
        return len([aid for aid, participants in self.auction_participants.items() if participants])
    
    def get_connected_users_count(self) -> int:
        """Get count of connected users"""
        return len(self.connected_users)
    
    def get_auction_participants_count(self, auction_id: int) -> int:
        """Get count of participants in specific auction"""
        return len(self.auction_participants.get(auction_id, set()))

# Global WebSocket server instance
websocket_server = None

def create_websocket_server(app: Flask, secret_key: str) -> AuctionWebSocketServer:
    """Create and configure WebSocket server"""
    global websocket_server
    websocket_server = AuctionWebSocketServer(app, secret_key)
    return websocket_server

def get_websocket_server() -> Optional[AuctionWebSocketServer]:
    """Get the global WebSocket server instance"""
    return websocket_server
