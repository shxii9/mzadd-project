"""
Comprehensive Test Suite for Mzadd Auction Platform
Tests all major functionality including API endpoints, business logic, and WebSocket operations
"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Test imports
import sys
sys.path.append('..')

from app import create_app
from models_enhanced import db, User, Item, Auction, Bid, UserRole, ItemStatus, AuctionStatus
from business_logic import revenue_manager, analytics_manager, profit_optimizer
from websocket_server import create_websocket_server

class MzaddTestCase(unittest.TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test environment"""
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Create test app
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{self.db_path}',
            'SECRET_KEY': 'test-secret-key',
            'WTF_CSRF_ENABLED': False
        })
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables
        db.create_all()
        
        # Create test users
        self.create_test_users()
        
        # Create WebSocket server for testing
        self.websocket_server = create_websocket_server(self.app, 'test-secret-key')
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def create_test_users(self):
        """Create test users for testing"""
        # Admin user
        self.admin_user = User(
            username='admin_test',
            email='admin@test.com',
            role=UserRole.ADMIN,
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_verified=True
        )
        self.admin_user.set_password('admin123')
        
        # Merchant user
        self.merchant_user = User(
            username='merchant_test',
            email='merchant@test.com',
            role=UserRole.MERCHANT,
            first_name='Merchant',
            last_name='User',
            is_active=True,
            is_verified=True,
            commission_rate=0.05
        )
        self.merchant_user.set_password('merchant123')
        
        # Bidder user
        self.bidder_user = User(
            username='bidder_test',
            email='bidder@test.com',
            role=UserRole.BIDDER,
            first_name='Bidder',
            last_name='User',
            is_active=True,
            is_verified=True
        )
        self.bidder_user.set_password('bidder123')
        
        db.session.add_all([self.admin_user, self.merchant_user, self.bidder_user])
        db.session.commit()
    
    def login_user(self, username, password):
        """Helper method to login user and get token"""
        response = self.client.post('/api/auth/login', 
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            return data.get('access_token')
        return None
    
    def get_auth_headers(self, token):
        """Helper method to get authorization headers"""
        return {'Authorization': f'Bearer {token}'}

class TestAuthentication(MzaddTestCase):
    """Test authentication and authorization"""
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register', 
            data=json.dumps({
                'username': 'newuser',
                'email': 'newuser@test.com',
                'password': 'password123',
                'first_name': 'New',
                'last_name': 'User',
                'role': 'bidder'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        
        # Verify user was created
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@test.com')
    
    def test_user_login(self):
        """Test user login"""
        token = self.login_user('admin_test', 'admin123')
        self.assertIsNotNone(token)
        
        # Test invalid credentials
        invalid_token = self.login_user('admin_test', 'wrongpassword')
        self.assertIsNone(invalid_token)
    
    def test_protected_route_access(self):
        """Test access to protected routes"""
        # Test without token
        response = self.client.get('/api/auth/users/me')
        self.assertEqual(response.status_code, 401)
        
        # Test with valid token
        token = self.login_user('admin_test', 'admin123')
        response = self.client.get('/api/auth/users/me', 
            headers=self.get_auth_headers(token)
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'admin_test')

class TestItemManagement(MzaddTestCase):
    """Test item creation and management"""
    
    def test_create_item(self):
        """Test item creation by merchant"""
        token = self.login_user('merchant_test', 'merchant123')
        
        response = self.client.post('/api/items', 
            data=json.dumps({
                'name': 'Test Item',
                'description': 'A test item for auction',
                'category': 'Electronics',
                'start_price': 100.0
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Item')
        
        # Verify item was created
        item = Item.query.filter_by(name='Test Item').first()
        self.assertIsNotNone(item)
        self.assertEqual(item.owner_id, self.merchant_user.id)
    
    def test_get_items(self):
        """Test retrieving items"""
        # Create a test item
        item = Item(
            name='Test Item',
            description='Test description',
            category='Electronics',
            start_price=100.0,
            owner_id=self.merchant_user.id,
            status=ItemStatus.ACTIVE
        )
        db.session.add(item)
        db.session.commit()
        
        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
    
    def test_unauthorized_item_creation(self):
        """Test that bidders cannot create items"""
        token = self.login_user('bidder_test', 'bidder123')
        
        response = self.client.post('/api/items', 
            data=json.dumps({
                'name': 'Unauthorized Item',
                'description': 'Should not be created',
                'category': 'Electronics',
                'start_price': 100.0
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 403)

class TestAuctionManagement(MzaddTestCase):
    """Test auction creation and management"""
    
    def setUp(self):
        super().setUp()
        
        # Create test item
        self.test_item = Item(
            name='Test Auction Item',
            description='Item for auction testing',
            category='Electronics',
            start_price=100.0,
            owner_id=self.merchant_user.id,
            status=ItemStatus.ACTIVE
        )
        db.session.add(self.test_item)
        db.session.commit()
    
    def test_create_auction(self):
        """Test auction creation"""
        token = self.login_user('merchant_test', 'merchant123')
        
        start_time = datetime.utcnow() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=24)
        
        response = self.client.post('/api/auctions', 
            data=json.dumps({
                'item_id': self.test_item.id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['item_id'], self.test_item.id)
        
        # Verify auction was created
        auction = Auction.query.filter_by(item_id=self.test_item.id).first()
        self.assertIsNotNone(auction)
        self.assertEqual(auction.status, AuctionStatus.SCHEDULED)
    
    def test_get_active_auctions(self):
        """Test retrieving active auctions"""
        # Create active auction
        auction = Auction(
            item_id=self.test_item.id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=23),
            current_price=self.test_item.start_price,
            status=AuctionStatus.ACTIVE
        )
        db.session.add(auction)
        db.session.commit()
        
        response = self.client.get('/api/auctions?status=active')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['status'], 'active')

class TestBiddingSystem(MzaddTestCase):
    """Test bidding functionality"""
    
    def setUp(self):
        super().setUp()
        
        # Create test item and auction
        self.test_item = Item(
            name='Bidding Test Item',
            description='Item for bidding tests',
            category='Electronics',
            start_price=100.0,
            owner_id=self.merchant_user.id,
            status=ItemStatus.ACTIVE
        )
        
        self.test_auction = Auction(
            item_id=self.test_item.id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=23),
            current_price=100.0,
            status=AuctionStatus.ACTIVE
        )
        
        db.session.add_all([self.test_item, self.test_auction])
        db.session.commit()
        
        # Update item reference
        self.test_auction.item_id = self.test_item.id
        db.session.commit()
    
    def test_place_valid_bid(self):
        """Test placing a valid bid"""
        token = self.login_user('bidder_test', 'bidder123')
        
        response = self.client.post(f'/api/auctions/{self.test_auction.id}/bids', 
            data=json.dumps({
                'amount': 150.0
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['amount'], 150.0)
        
        # Verify bid was created and auction updated
        bid = Bid.query.filter_by(auction_id=self.test_auction.id).first()
        self.assertIsNotNone(bid)
        self.assertEqual(bid.amount, 150.0)
        
        # Refresh auction
        db.session.refresh(self.test_auction)
        self.assertEqual(self.test_auction.current_price, 150.0)
    
    def test_invalid_bid_amount(self):
        """Test placing bid with invalid amount"""
        token = self.login_user('bidder_test', 'bidder123')
        
        # Bid too low
        response = self.client.post(f'/api/auctions/{self.test_auction.id}/bids', 
            data=json.dumps({
                'amount': 99.0  # Lower than current price
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_merchant_cannot_bid_on_own_item(self):
        """Test that merchants cannot bid on their own items"""
        token = self.login_user('merchant_test', 'merchant123')
        
        response = self.client.post(f'/api/auctions/{self.test_auction.id}/bids', 
            data=json.dumps({
                'amount': 150.0
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        self.assertEqual(response.status_code, 400)

class TestBusinessLogic(MzaddTestCase):
    """Test business logic and revenue management"""
    
    def setUp(self):
        super().setUp()
        
        # Create completed auction for testing
        self.test_item = Item(
            name='Revenue Test Item',
            description='Item for revenue testing',
            category='Electronics',
            start_price=100.0,
            owner_id=self.merchant_user.id,
            status=ItemStatus.ACTIVE
        )
        
        self.test_auction = Auction(
            item_id=self.test_item.id,
            start_time=datetime.utcnow() - timedelta(hours=25),
            end_time=datetime.utcnow() - timedelta(hours=1),
            current_price=500.0,
            status=AuctionStatus.CLOSED,
            total_bids=10,
            unique_bidders=5
        )
        
        self.winning_bid = Bid(
            auction_id=self.test_auction.id,
            bidder_id=self.bidder_user.id,
            amount=500.0,
            timestamp=datetime.utcnow() - timedelta(hours=2),
            is_valid=True
        )
        
        db.session.add_all([self.test_item, self.test_auction, self.winning_bid])
        db.session.commit()
        
        # Set winning bid
        self.test_auction.winning_bid_id = self.winning_bid.id
        db.session.commit()
    
    def test_commission_calculation(self):
        """Test commission calculation"""
        commission = revenue_manager.calculate_commission(500.0, 0.05)
        self.assertEqual(commission, 25.0)  # 5% of 500
        
        # Test with custom rate
        commission = revenue_manager.calculate_commission(1000.0, 0.03)
        self.assertEqual(commission, 30.0)  # 3% of 1000
    
    def test_auction_completion_processing(self):
        """Test processing completed auction"""
        result = revenue_manager.process_auction_completion(self.test_auction.id)
        
        self.assertTrue(result['success'])
        self.assertIn('transaction', result)
        
        transaction = result['transaction']
        self.assertEqual(transaction['final_price'], 500.0)
        self.assertEqual(transaction['commission'], 25.0)  # 5% commission
        self.assertEqual(transaction['merchant_earnings'], 475.0)
    
    def test_analytics_generation(self):
        """Test analytics generation"""
        result = analytics_manager.get_revenue_analytics()
        
        self.assertTrue(result['success'])
        self.assertIn('analytics', result)
        
        analytics = result['analytics']
        self.assertIn('summary', analytics)
        self.assertIn('total_revenue', analytics['summary'])
        self.assertIn('total_commission', analytics['summary'])
    
    def test_commission_rate_optimization(self):
        """Test commission rate optimization"""
        result = profit_optimizer.suggest_optimal_commission_rate(self.merchant_user.id)
        
        self.assertTrue(result['success'])
        self.assertIn('recommendation', result)
        
        recommendation = result['recommendation']
        self.assertIn('suggested_rate', recommendation)
        self.assertIn('reason', recommendation)

class TestWebSocketFunctionality(MzaddTestCase):
    """Test WebSocket real-time functionality"""
    
    def test_websocket_server_creation(self):
        """Test WebSocket server initialization"""
        self.assertIsNotNone(self.websocket_server)
        self.assertEqual(self.websocket_server.get_connected_users_count(), 0)
        self.assertEqual(self.websocket_server.get_active_auctions_count(), 0)
    
    def test_bid_validation(self):
        """Test bid validation logic"""
        # Create test auction
        item = Item(
            name='WebSocket Test Item',
            description='Test item',
            category='Electronics',
            start_price=100.0,
            owner_id=self.merchant_user.id,
            status=ItemStatus.ACTIVE
        )
        
        auction = Auction(
            item_id=item.id,
            start_time=datetime.utcnow() - timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=23),
            current_price=150.0,
            status=AuctionStatus.ACTIVE
        )
        
        db.session.add_all([item, auction])
        db.session.commit()
        
        # Test valid bid
        result = self.websocket_server.validate_bid(
            self.bidder_user.id, auction.id, 200.0
        )
        self.assertTrue(result['valid'])
        
        # Test invalid bid (too low)
        result = self.websocket_server.validate_bid(
            self.bidder_user.id, auction.id, 140.0
        )
        self.assertFalse(result['valid'])
        
        # Test merchant bidding on own item
        result = self.websocket_server.validate_bid(
            self.merchant_user.id, auction.id, 200.0
        )
        self.assertFalse(result['valid'])

class TestSecurityFeatures(MzaddTestCase):
    """Test security features and protections"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        user = User(username='security_test', email='security@test.com')
        user.set_password('testpassword123')
        
        # Password should be hashed
        self.assertNotEqual(user.password_hash, 'testpassword123')
        
        # Verification should work
        self.assertTrue(user.check_password('testpassword123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_input_validation(self):
        """Test input validation and sanitization"""
        token = self.login_user('merchant_test', 'merchant123')
        
        # Test with malicious input
        response = self.client.post('/api/items', 
            data=json.dumps({
                'name': '<script>alert("xss")</script>',
                'description': 'SELECT * FROM users',
                'category': 'Electronics',
                'start_price': 'invalid_price'
            }),
            content_type='application/json',
            headers=self.get_auth_headers(token)
        )
        
        # Should return validation error
        self.assertEqual(response.status_code, 400)
    
    def test_rate_limiting_simulation(self):
        """Test rate limiting (simulated)"""
        token = self.login_user('bidder_test', 'bidder123')
        
        # Make multiple rapid requests
        responses = []
        for _ in range(10):
            response = self.client.get('/api/items', 
                headers=self.get_auth_headers(token)
            )
            responses.append(response.status_code)
        
        # All should succeed in test environment
        # In production, rate limiting would kick in
        self.assertTrue(all(status == 200 for status in responses))

def run_comprehensive_tests():
    """Run all test suites"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestAuthentication,
        TestItemManagement,
        TestAuctionManagement,
        TestBiddingSystem,
        TestBusinessLogic,
        TestWebSocketFunctionality,
        TestSecurityFeatures
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_comprehensive_tests()
    exit(0 if success else 1)
