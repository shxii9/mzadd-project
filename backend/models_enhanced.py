from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, func
import secrets
import enum

db = SQLAlchemy()
bcrypt = Bcrypt()

class UserRole(enum.Enum):
    """User roles enumeration for better type safety."""
    ADMIN = "admin"
    MERCHANT = "merchant"
    BIDDER = "bidder"

class AuctionStatus(enum.Enum):
    """Auction status enumeration."""
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class ItemStatus(enum.Enum):
    """Item status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
    REJECTED = "rejected"

class User(db.Model):
    """Enhanced User model with security features."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.BIDDER)
    
    # Profile information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Security fields
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), nullable=True)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Audit fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0)
    
    # Business fields for merchants
    commission_rate = db.Column(db.Float, default=0.05)  # 5% default commission
    total_earnings = db.Column(db.Float, default=0.0)
    
    # Relationships
    items = db.relationship('Item', backref='owner', lazy=True, cascade="all, delete-orphan")
    bids = db.relationship('Bid', backref='bidder', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Set password with enhanced security."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check password with timing attack protection."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def generate_verification_token(self):
        """Generate email verification token."""
        self.verification_token = secrets.token_urlsafe(32)
        return self.verification_token
    
    def generate_reset_token(self, expires_in=3600):
        """Generate password reset token."""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(seconds=expires_in)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify password reset token."""
        if not self.reset_token or not self.reset_token_expires:
            return False
        if datetime.utcnow() > self.reset_token_expires:
            return False
        return self.reset_token == token
    
    @hybrid_property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def update_login_info(self):
        """Update login information."""
        self.last_login = datetime.utcnow()
        self.login_count += 1
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary."""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'role': self.role.value,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if self.role == UserRole.MERCHANT and include_sensitive:
            data.update({
                'commission_rate': self.commission_rate,
                'total_earnings': self.total_earnings
            })
        
        return data

    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    """Enhanced Item model with better validation."""
    __tablename__ = 'item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    
    # Pricing
    start_price = db.Column(db.Float, nullable=False)
    reserve_price = db.Column(db.Float, nullable=True)  # Minimum selling price
    
    # Media
    image_url = db.Column(db.String(255), nullable=True)
    additional_images = db.Column(db.JSON, nullable=True)  # Array of image URLs
    
    # Status and ownership
    status = db.Column(db.Enum(ItemStatus), nullable=False, default=ItemStatus.PENDING)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Audit fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Admin review fields
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    # Relationships
    auctions = db.relationship('Auction', backref='item', lazy=True, cascade="all, delete-orphan")
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_items')
    
    def to_dict(self, include_owner=False):
        """Convert item to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'start_price': self.start_price,
            'reserve_price': self.reserve_price,
            'image_url': self.image_url,
            'additional_images': self.additional_images or [],
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_owner:
            data['owner'] = self.owner.to_dict()
        
        return data

    def __repr__(self):
        return f'<Item {self.name}>'

class Auction(db.Model):
    """Enhanced Auction model with business logic."""
    __tablename__ = 'auction'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # Timing
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    extended_count = db.Column(db.Integer, default=0)  # Number of extensions
    
    # Pricing
    current_price = db.Column(db.Float, nullable=False)
    winning_bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'), nullable=True)
    
    # Status
    status = db.Column(db.Enum(AuctionStatus), nullable=False, default=AuctionStatus.SCHEDULED)
    
    # Business fields
    total_bids = db.Column(db.Integer, default=0)
    unique_bidders = db.Column(db.Integer, default=0)
    
    # Audit fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bids = db.relationship('Bid', backref='auction', lazy='dynamic', cascade="all, delete-orphan",
                          foreign_keys='Bid.auction_id')
    winning_bid = db.relationship('Bid', foreign_keys=[winning_bid_id], post_update=True)
    
    @hybrid_property
    def is_active(self):
        """Check if auction is currently active."""
        now = datetime.utcnow()
        return (self.status == AuctionStatus.ACTIVE and 
                self.start_time <= now <= self.end_time)
    
    @hybrid_property
    def time_remaining(self):
        """Get time remaining in seconds."""
        if not self.is_active:
            return 0
        return max(0, int((self.end_time - datetime.utcnow()).total_seconds()))
    
    def extend_auction(self, extension_time=300):
        """Extend auction by specified time (default 5 minutes)."""
        if self.is_active and self.time_remaining < extension_time:
            self.end_time = datetime.utcnow() + timedelta(seconds=extension_time)
            self.extended_count += 1
            return True
        return False
    
    def update_status(self):
        """Update auction status based on current time."""
        now = datetime.utcnow()
        
        if self.status == AuctionStatus.SCHEDULED and now >= self.start_time:
            self.status = AuctionStatus.ACTIVE
        elif self.status == AuctionStatus.ACTIVE and now > self.end_time:
            self.status = AuctionStatus.CLOSED
            # Update item status
            if self.winning_bid_id:
                self.item.status = ItemStatus.SOLD
            else:
                self.item.status = ItemStatus.EXPIRED
    
    def to_dict(self, include_item=False, include_bids=False):
        """Convert auction to dictionary."""
        data = {
            'id': self.id,
            'item_id': self.item_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'current_price': self.current_price,
            'status': self.status.value,
            'total_bids': self.total_bids,
            'unique_bidders': self.unique_bidders,
            'time_remaining': self.time_remaining,
            'extended_count': self.extended_count,
            'created_at': self.created_at.isoformat()
        }
        
        if include_item:
            data['item'] = self.item.to_dict()
        
        if include_bids:
            data['recent_bids'] = [bid.to_dict() for bid in self.bids.order_by(Bid.timestamp.desc()).limit(10)]
        
        if self.winning_bid:
            data['winning_bid'] = self.winning_bid.to_dict()
        
        return data

    def __repr__(self):
        return f'<Auction {self.id} for Item {self.item_id}>'

class Bid(db.Model):
    """Enhanced Bid model with validation."""
    __tablename__ = 'bid'
    
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id', ondelete='CASCADE'), nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Validation fields
    is_valid = db.Column(db.Boolean, default=True)
    validation_message = db.Column(db.String(255), nullable=True)
    
    def to_dict(self, include_bidder=False):
        """Convert bid to dictionary."""
        data = {
            'id': self.id,
            'auction_id': self.auction_id,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'is_valid': self.is_valid
        }
        
        if include_bidder:
            data['bidder'] = self.bidder.to_dict()
        else:
            data['bidder_name'] = self.bidder.username
        
        return data

    def __repr__(self):
        return f'<Bid {self.id} of {self.amount} on Auction {self.auction_id}>'

class Notification(db.Model):
    """Notification system for users."""
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'bid', 'auction', 'system'
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Optional reference to related objects
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    
    def to_dict(self):
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'auction_id': self.auction_id,
            'item_id': self.item_id
        }

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'

# Event listeners for automatic updates
@event.listens_for(Bid, 'after_insert')
def update_auction_after_bid(mapper, connection, target):
    """Update auction statistics after new bid."""
    auction_table = Auction.__table__
    bid_table = Bid.__table__
    
    # Update current price and winning bid
    connection.execute(
        auction_table.update()
        .where(auction_table.c.id == target.auction_id)
        .values(
            current_price=target.amount,
            winning_bid_id=target.id,
            updated_at=datetime.utcnow()
        )
    )
    
    # Update total bids count
    total_bids = connection.execute(
        func.count(bid_table.c.id).select()
        .where(bid_table.c.auction_id == target.auction_id)
    ).scalar()
    
    # Update unique bidders count
    unique_bidders = connection.execute(
        func.count(func.distinct(bid_table.c.bidder_id)).select()
        .where(bid_table.c.auction_id == target.auction_id)
    ).scalar()
    
    connection.execute(
        auction_table.update()
        .where(auction_table.c.id == target.auction_id)
        .values(
            total_bids=total_bids,
            unique_bidders=unique_bidders
        )
    )
