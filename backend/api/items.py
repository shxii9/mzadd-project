from flask import Blueprint, request, jsonify, g
from models import db, Item
from api.decorators import token_required

items_bp = Blueprint('items', __name__)

@items_bp.route('', methods=['POST'])
@token_required(role='merchant')
def create_item():
    data = request.get_json()
    current_user = g.current_user

    new_item = Item(
        name=data.get('name'),
        description=data.get('description'),
        start_price=data.get('start_price'),
        image_url=data.get('image_url'),
        owner_id=current_user.id
    )

    if not new_item.name or not new_item.start_price:
        return jsonify({"message": "Name and start price are required"}), 400

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "id": new_item.id,
        "name": new_item.name,
        "description": new_item.description,
        "start_price": new_item.start_price,
        "status": new_item.status
    }), 201

@items_bp.route('', methods=['GET'])
@token_required(role='merchant')
def get_items():
    current_user = g.current_user
    items = Item.query.filter_by(owner_id=current_user.id).all()
    
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "status": item.status,
        "start_price": item.start_price
    } for item in items]), 200

@items_bp.route('/<int:id>', methods=['GET'])
@token_required(role='merchant')
def get_item(id):
    current_user = g.current_user
    item = Item.query.filter_by(id=id, owner_id=current_user.id).first_or_404()
    
    return jsonify({
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "start_price": item.start_price,
        "image_url": item.image_url,
        "status": item.status
    }), 200

@items_bp.route('/<int:id>', methods=['PUT'])
@token_required(role='merchant')
def update_item(id):
    current_user = g.current_user
    item = Item.query.filter_by(id=id, owner_id=current_user.id).first_or_404()

    if item.status != 'pending':
        return jsonify({"message": "Cannot update item after auction has started"}), 403

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.start_price = data.get('start_price', item.start_price)
    item.image_url = data.get('image_url', item.image_url)
    
    db.session.commit()
    return jsonify({
        "id": item.id, 
        "name": item.name,
        "description": item.description,
        "start_price": item.start_price
    }), 200

@items_bp.route('/<int:id>', methods=['DELETE'])
@token_required(role='merchant')
def delete_item(id):
    current_user = g.current_user
    item = Item.query.filter_by(id=id, owner_id=current_user.id).first_or_404()

    if item.status != 'pending':
        return jsonify({"message": "Cannot delete item after auction has started"}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
