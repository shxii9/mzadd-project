from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
from models import User

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'message': 'Bearer token malformed'}), 401

            if not token:
                return jsonify({'message': 'Token is missing'}), 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['id'])
                if not current_user:
                    return jsonify({'message': 'User not found'}), 401
                g.current_user = current_user
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 401

            if role and g.current_user.role != role:
                return jsonify({'message': f'Access denied: requires {role} role'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
