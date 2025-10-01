from flask import Blueprint, request, jsonify, g, current_app
from models import db, Item, Auction, Bid, User
from api.decorators import token_required
from datetime import datetime

auctions_bp = Blueprint('auctions', __name__)

def get_socketio_instance():
    from app import socketio
    return socketio

@auctions_bp.route('', methods=['POST'])
@token_required(role='merchant')
def create_auction():
    data = request.get_json()
    item_id = data.get('item_id')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')

    if not all([item_id, start_time_str, end_time_str]):
        return jsonify({"message": "Missing item_id, start_time, or end_time"}), 400

    item = Item.query.filter_by(id=item_id, owner_id=g.current_user.id).first()
    if not item:
        return jsonify({"message": "Item not found or you are not the owner"}), 404

    if Auction.query.filter_by(item_id=item_id).first():
        return jsonify({"message": "Auction for this item already exists"}), 409

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"message": "Invalid datetime format. Use ISO format."}), 400

    new_auction = Auction(
        item_id=item.id,
        start_time=start_time,
        end_time=end_time,
        current_price=item.start_price
    )
    
    item.status = 'active'
    db.session.add(new_auction)
    db.session.commit()

    return jsonify({
        "id": new_auction.id,
        "item_id": new_auction.item_id,
        "status": "scheduled"
    }), 201

@auctions_bp.route('/active', methods=['GET'])
def get_active_auctions():
    now = datetime.utcnow()
    active_auctions = Auction.query.filter(Auction.start_time <= now, Auction.end_time >= now, Auction.status == 'active').all()

    return jsonify([{
        "id": auction.id,
        "item_name": auction.item.name,
        "item_image_url": auction.item.image_url,
        "current_price": auction.current_price,
        "end_time": auction.end_time.isoformat()
    } for auction in active_auctions]), 200

@auctions_bp.route('/<int:id>', methods=['GET'])
def get_auction_details(id):
    auction = Auction.query.get_or_404(id)
    bids = auction.bids.order_by(Bid.timestamp.desc()).all()

    return jsonify({
        "id": auction.id,
        "item_details": {
            "name": auction.item.name,
            "description": auction.item.description,
            "image_url": auction.item.image_url
        },
        "start_time": auction.start_time.isoformat(),
        "end_time": auction.end_time.isoformat(),
        "current_price": auction.current_price,
        "status": auction.status,
        "bids": [{
            "bidder_name": bid.bidder.username,
            "amount": bid.amount,
            "timestamp": bid.timestamp.isoformat()
        } for bid in bids]
    }), 200

@auctions_bp.route('/<int:id>/bids', methods=['GET'])
def get_auction_bids(id):
    auction = Auction.query.get_or_404(id)
    bids = auction.bids.order_by(Bid.timestamp.desc()).all()
    
    return jsonify([{
        "bidder_name": bid.bidder.username,
        "amount": bid.amount,
        "timestamp": bid.timestamp.isoformat()
    } for bid in bids]), 200

@auctions_bp.route('/<int:id>/bid', methods=['POST'])
@token_required(role='bidder')
def place_bid(id):
    auction = Auction.query.get_or_404(id)
    now = datetime.utcnow()

    if auction.status != 'active' or not (auction.start_time <= now < auction.end_time):
        return jsonify({"message": "Auction is not active"}), 403

    data = request.get_json()
    amount = data.get('amount')

    if not amount or not isinstance(amount, (int, float)):
        return jsonify({"message": "Invalid bid amount"}), 400

    if amount <= auction.current_price:
        return jsonify({"message": "Bid must be higher than the current price"}), 400
    
    if g.current_user.id == auction.item.owner_id:
        return jsonify({"message": "Owners cannot bid on their own items"}), 403

    new_bid = Bid(
        auction_id=auction.id,
        bidder_id=g.current_user.id,
        amount=amount
    )

    auction.current_price = amount
    db.session.add(new_bid)
    db.session.commit()
    
    auction.winning_bid_id = new_bid.id
    db.session.commit()

    socketio = get_socketio_instance()
    socketio.emit('new_bid', {
        'type': 'new_bid',
        'data': {
            'auction_id': auction.id,
            'new_price': auction.current_price,
            'bidder_name': g.current_user.username,
            'timestamp': new_bid.timestamp.isoformat()
        }
    }, room=f'auction-{auction.id}')

    return jsonify({"message": "Bid placed successfully"}), 201
