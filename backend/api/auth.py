# backend/api/auth.py
from flask import Blueprint, request, jsonify
from models_enhanced import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role.value})
        return jsonify(access_token=access_token)
        
    return jsonify({"msg": "Bad username or password"}), 401
