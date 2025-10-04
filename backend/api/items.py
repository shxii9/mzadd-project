# backend/api/items.py
from flask import Blueprint, request, jsonify

# Use explicit relative imports
from models_enhanced import Item
from extensions import db

items_bp = Blueprint('items_bp', __name__)

@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict(include_owner=True)), 200

@items_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('start_price') or not data.get('owner_id'):
        return jsonify({'message': 'Missing required fields'}), 400

    new_item = Item(
        name=data['name'],
        description=data.get('description', ''),
        category=data.get('category'),
        start_price=data['start_price'],
        owner_id=data['owner_id']
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201

