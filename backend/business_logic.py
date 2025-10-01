"""
Business Logic Module for Mzadd Auction Platform
Handles revenue management, commission calculations, and profit distribution
"""

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import func
from models_enhanced import db, User, Auction, Bid, Item, UserRole, AuctionStatus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RevenueManager:
    """Manages all revenue-related operations for the platform"""
    
    def __init__(self):
        self.default_commission_rate = Decimal('0.05')  # 5% default commission
        self.merchant_registration_fee = Decimal('10.00')  # 10 KWD registration fee
        self.premium_listing_fee = Decimal('5.00')  # Premium listing fee
        self.featured_auction_fee = Decimal('15.00')  # Featured auction fee
    
    def calculate_commission(self, final_price, merchant_commission_rate=None):
        """Calculate commission from auction sale"""
        if merchant_commission_rate is None:
            commission_rate = self.default_commission_rate
        else:
            commission_rate = Decimal(str(merchant_commission_rate))
        
        commission = (Decimal(str(final_price)) * commission_rate).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        return float(commission)
    
    def process_auction_completion(self, auction_id):
        """Process completed auction and calculate all fees"""
        try:
            auction = Auction.query.get(auction_id)
            if not auction or auction.status != AuctionStatus.CLOSED:
                return {'success': False, 'message': 'Invalid auction or not closed'}
            
            if not auction.winning_bid_id:
                return {'success': False, 'message': 'No winning bid found'}
            
            merchant = auction.item.owner
            final_price = auction.current_price
            
            # Calculate commission
            commission = self.calculate_commission(final_price, merchant.commission_rate)
            
            # Calculate merchant earnings (final price - commission)
            merchant_earnings = final_price - commission
            
            # Update merchant total earnings
            merchant.total_earnings += merchant_earnings
            
            # Create transaction record
            transaction = {
                'auction_id': auction_id,
                'merchant_id': merchant.id,
                'final_price': final_price,
                'commission': commission,
                'merchant_earnings': merchant_earnings,
                'processed_at': datetime.utcnow()
            }
            
            # Log the transaction
            logger.info(f"Processed auction {auction_id}: Final price: {final_price} KWD, "
                       f"Commission: {commission} KWD, Merchant earnings: {merchant_earnings} KWD")
            
            db.session.commit()
            
            return {
                'success': True,
                'transaction': transaction
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing auction completion: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def charge_merchant_registration_fee(self, merchant_id):
        """Charge registration fee for new merchants"""
        try:
            merchant = User.query.get(merchant_id)
            if not merchant or merchant.role != UserRole.MERCHANT:
                return {'success': False, 'message': 'Invalid merchant'}
            
            # In a real implementation, this would integrate with payment gateway
            # For now, we'll just record the fee
            fee_record = {
                'merchant_id': merchant_id,
                'fee_type': 'registration',
                'amount': float(self.merchant_registration_fee),
                'charged_at': datetime.utcnow(),
                'status': 'pending'  # Would be 'paid' after payment confirmation
            }
            
            logger.info(f"Registration fee charged to merchant {merchant_id}: {self.merchant_registration_fee} KWD")
            
            return {
                'success': True,
                'fee_record': fee_record
            }
            
        except Exception as e:
            logger.error(f"Error charging registration fee: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def charge_premium_listing_fee(self, item_id):
        """Charge premium listing fee for featured items"""
        try:
            item = Item.query.get(item_id)
            if not item:
                return {'success': False, 'message': 'Item not found'}
            
            fee_record = {
                'merchant_id': item.owner_id,
                'item_id': item_id,
                'fee_type': 'premium_listing',
                'amount': float(self.premium_listing_fee),
                'charged_at': datetime.utcnow(),
                'status': 'pending'
            }
            
            logger.info(f"Premium listing fee charged for item {item_id}: {self.premium_listing_fee} KWD")
            
            return {
                'success': True,
                'fee_record': fee_record
            }
            
        except Exception as e:
            logger.error(f"Error charging premium listing fee: {str(e)}")
            return {'success': False, 'message': str(e)}

class AnalyticsManager:
    """Manages analytics and reporting for business intelligence"""
    
    def get_revenue_analytics(self, start_date=None, end_date=None):
        """Get comprehensive revenue analytics"""
        try:
            if not start_date:
                start_date = datetime.utcnow() - timedelta(days=30)
            if not end_date:
                end_date = datetime.utcnow()
            
            # Get completed auctions in date range
            completed_auctions = Auction.query.filter(
                Auction.status == AuctionStatus.CLOSED,
                Auction.updated_at >= start_date,
                Auction.updated_at <= end_date,
                Auction.winning_bid_id.isnot(None)
            ).all()
            
            total_revenue = sum(auction.current_price for auction in completed_auctions)
            total_commission = sum(
                RevenueManager().calculate_commission(
                    auction.current_price, 
                    auction.item.owner.commission_rate
                ) for auction in completed_auctions
            )
            
            # Calculate daily revenue breakdown
            daily_revenue = {}
            for auction in completed_auctions:
                date_key = auction.updated_at.date().isoformat()
                if date_key not in daily_revenue:
                    daily_revenue[date_key] = {
                        'total_sales': 0,
                        'commission': 0,
                        'auction_count': 0
                    }
                
                daily_revenue[date_key]['total_sales'] += auction.current_price
                daily_revenue[date_key]['commission'] += RevenueManager().calculate_commission(
                    auction.current_price, auction.item.owner.commission_rate
                )
                daily_revenue[date_key]['auction_count'] += 1
            
            # Top performing categories
            category_performance = {}
            for auction in completed_auctions:
                category = auction.item.category or 'Other'
                if category not in category_performance:
                    category_performance[category] = {
                        'total_sales': 0,
                        'auction_count': 0,
                        'avg_price': 0
                    }
                
                category_performance[category]['total_sales'] += auction.current_price
                category_performance[category]['auction_count'] += 1
                category_performance[category]['avg_price'] = (
                    category_performance[category]['total_sales'] / 
                    category_performance[category]['auction_count']
                )
            
            # Top merchants by revenue
            merchant_performance = {}
            for auction in completed_auctions:
                merchant_id = auction.item.owner_id
                merchant_name = auction.item.owner.full_name or auction.item.owner.username
                
                if merchant_id not in merchant_performance:
                    merchant_performance[merchant_id] = {
                        'name': merchant_name,
                        'total_sales': 0,
                        'auction_count': 0,
                        'commission_paid': 0
                    }
                
                merchant_performance[merchant_id]['total_sales'] += auction.current_price
                merchant_performance[merchant_id]['auction_count'] += 1
                merchant_performance[merchant_id]['commission_paid'] += RevenueManager().calculate_commission(
                    auction.current_price, auction.item.owner.commission_rate
                )
            
            return {
                'success': True,
                'analytics': {
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    },
                    'summary': {
                        'total_revenue': float(total_revenue),
                        'total_commission': float(total_commission),
                        'total_auctions': len(completed_auctions),
                        'average_sale_price': float(total_revenue / len(completed_auctions)) if completed_auctions else 0
                    },
                    'daily_revenue': daily_revenue,
                    'category_performance': category_performance,
                    'merchant_performance': merchant_performance
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating revenue analytics: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_user_analytics(self):
        """Get user growth and engagement analytics"""
        try:
            # Total users by role
            user_counts = db.session.query(
                User.role, func.count(User.id)
            ).group_by(User.role).all()
            
            # User registration trend (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            daily_registrations = db.session.query(
                func.date(User.created_at).label('date'),
                func.count(User.id).label('count')
            ).filter(
                User.created_at >= thirty_days_ago
            ).group_by(func.date(User.created_at)).all()
            
            # Active users (users who logged in last 7 days)
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            active_users = User.query.filter(
                User.last_login >= seven_days_ago
            ).count()
            
            return {
                'success': True,
                'analytics': {
                    'user_counts': {role.value: count for role, count in user_counts},
                    'daily_registrations': [
                        {'date': date.isoformat(), 'count': count} 
                        for date, count in daily_registrations
                    ],
                    'active_users_7_days': active_users,
                    'total_users': User.query.count()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating user analytics: {str(e)}")
            return {'success': False, 'message': str(e)}

class ProfitOptimizer:
    """Optimizes profit through dynamic pricing and recommendations"""
    
    def suggest_optimal_commission_rate(self, merchant_id):
        """Suggest optimal commission rate based on merchant performance"""
        try:
            merchant = User.query.get(merchant_id)
            if not merchant or merchant.role != UserRole.MERCHANT:
                return {'success': False, 'message': 'Invalid merchant'}
            
            # Get merchant's auction history
            merchant_auctions = Auction.query.join(Item).filter(
                Item.owner_id == merchant_id,
                Auction.status == AuctionStatus.CLOSED,
                Auction.winning_bid_id.isnot(None)
            ).all()
            
            if not merchant_auctions:
                return {
                    'success': True,
                    'recommendation': {
                        'suggested_rate': 0.05,  # Default rate
                        'reason': 'No auction history available, using default rate'
                    }
                }
            
            # Calculate performance metrics
            total_sales = sum(auction.current_price for auction in merchant_auctions)
            avg_sale_price = total_sales / len(merchant_auctions)
            success_rate = len(merchant_auctions) / len(merchant.items)  # Simplified metric
            
            # Dynamic commission rate based on performance
            base_rate = 0.05
            
            # High performers get lower rates
            if success_rate > 0.8 and avg_sale_price > 500:
                suggested_rate = 0.03  # 3% for top performers
                reason = 'High performance merchant - reduced commission rate'
            elif success_rate > 0.6 and avg_sale_price > 200:
                suggested_rate = 0.04  # 4% for good performers
                reason = 'Good performance merchant - slightly reduced rate'
            elif success_rate < 0.3 or avg_sale_price < 50:
                suggested_rate = 0.07  # 7% for underperformers (incentive to improve)
                reason = 'Performance improvement needed - higher commission rate'
            else:
                suggested_rate = base_rate
                reason = 'Standard commission rate based on current performance'
            
            return {
                'success': True,
                'recommendation': {
                    'current_rate': float(merchant.commission_rate),
                    'suggested_rate': suggested_rate,
                    'reason': reason,
                    'performance_metrics': {
                        'total_sales': float(total_sales),
                        'avg_sale_price': float(avg_sale_price),
                        'success_rate': float(success_rate),
                        'total_auctions': len(merchant_auctions)
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error suggesting commission rate: {str(e)}")
            return {'success': False, 'message': str(e)}

# Initialize managers
revenue_manager = RevenueManager()
analytics_manager = AnalyticsManager()
profit_optimizer = ProfitOptimizer()
