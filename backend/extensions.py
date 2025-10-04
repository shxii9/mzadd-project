# backend/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO # <--- THIS LINE WAS MISSING

# Create extension instances
db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO(cors_allowed_origins="*", async_mode='gevent') # <--- THIS LINE WAS MISSING
