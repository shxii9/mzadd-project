# backend/api/auctions.py
from flask import Blueprint, request, jsonify

# Use explicit relative imports
from models_enhanced import Auction, Bid
from extensions import db

auctions_bp = Blueprint('auctions_bp', __name__)

@auctions_bp.route('/', methods=['GET'])
def get_auctions():
    auctions = Auction.query.filter_by(status='ACTIVE').all()
    return jsonify([auction.to_dict(include_item=True) for auction in auctions]), 200

@auctions_bp.route('/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    return jsonify(auction.to_dict(include_item=True, include_bids=True)), 200

@auctions_bp.route('/<int:auction_id>/bids', methods=['POST'])
def place_bid(auction_id):
    data = request.get_json()
    auction = Auction.query.get_or_404(auction_id)

    if not data or not data.get('amount') or not data.get('bidder_id'):
        return jsonify({'message': 'Missing amount or bidder_id'}), 400

    if data['amount'] <= auction.current_price:
        return jsonify({'message': 'Bid must be higher than the current price'}), 400

    new_bid = Bid(
        auction_id=auction_id,
        bidder_id=data['bidder_id'],
        amount=data['amount']
    )
    
    # The event listener will update the auction's price and stats
    db.session.add(new_bid)
    db.session.commit()

    # In a real app, you would emit a socketio event here to update all clients
    # socketio.emit('new_bid', {'auction_id': auction_id, 'bid': new_bid.to_dict()}, room=f'auction-{auction_id}')

    return jsonify(new_bid.to_dict()), 201
