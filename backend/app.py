from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room
from config import Config
from models import db, bcrypt

socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)

    from api.auth import auth_bp
    from api.items import items_bp
    from api.auctions import auctions_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(auctions_bp, url_prefix='/api/auctions')

    @app.route('/')
    def index():
        return "BidFlow API Server is running."

    @socketio.on('join')
    def on_join(data):
        auction_id = data.get('auction_id')
        if auction_id:
            room = f'auction-{auction_id}'
            join_room(room)
            print(f"Client joined room: {room}")

    @socketio.on('leave')
    def on_leave(data):
        auction_id = data.get('auction_id')
        if auction_id:
            room = f'auction-{auction_id}'
            leave_room(room)
            print(f"Client left room: {room}")
            
    @socketio.on('connect')
    def on_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def on_disconnect():
        print('Client disconnected')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
