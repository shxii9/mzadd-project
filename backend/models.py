from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False, default='bidder') # 'merchant' or 'bidder'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('Item', backref='owner', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    start_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending') # 'pending', 'active', 'sold', 'expired'
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    auctions = db.relationship('Auction', backref='item', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Item {self.name}>'

class Auction(db.Model):
    __tablename__ = 'auction'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False, unique=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    winning_bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='scheduled') # 'scheduled', 'active', 'closed'
    
    bids = db.relationship('Bid', backref='auction', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Auction {self.id} for Item {self.item_id}>'

class Bid(db.Model):
    __tablename__ = 'bid'
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id', ondelete='CASCADE'), nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Bid {self.id} of {self.amount} on Auction {self.auction_id}>'
