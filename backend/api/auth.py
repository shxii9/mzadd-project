from flask import Blueprint, request, jsonify, current_app, g
from models import db, User
from datetime import datetime, timedelta
import jwt
from api.decorators import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'bidder')

    if not all([username, password, email]):
        return jsonify({"message": "Missing username, password, or email"}), 400

    if role not in ['merchant', 'bidder']:
        return jsonify({"message": "Invalid role specified"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = jwt.encode({
            'id': user.id,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'access_token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/users/me', methods=['GET'])
@token_required()
def get_current_user():
    user = g.current_user
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200
