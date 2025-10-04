# backend/app.py
from flask import Flask
from flask_cors import CORS

# --- 1. استيراد الإضافات والتهيئة ---
# لاحظ: لا توجد نقاط هنا. هذا هو الشكل الصحيح.
from extensions import db, bcrypt, socketio
from config import Config

def create_app(config_class=Config):
    """
    Application Factory:
    This pattern allows us to create instances of the app with different configurations,
    which is great for testing and scalability.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- 2. تهيئة الإضافات مع التطبيق ---
    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app)

    # --- 3. تسجيل Blueprints ---
    # لاحظ: لا توجد نقاط هنا أيضًا. هذا هو الشكل الصحيح.
    from api.auth import auth_bp
    # from api.items import items_bp      # TODO: Uncomment when items API is implemented
    # from api.auctions import auctions_bp  # TODO: Uncomment when auctions API is implemented
    from api.merchant import merchant_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(items_bp, url_prefix='/api/items')      # TODO: Uncomment when items API is implemented
    # app.register_blueprint(auctions_bp, url_prefix='/api/auctions')  # TODO: Uncomment when auctions API is implemented
    app.register_blueprint(merchant_bp, url_prefix='/api')

    # --- 4. أوامر مخصصة (Custom CLI Commands) ---
    @app.cli.command("init-db")
    def init_db_command():
        """Creates the database tables."""
        db.create_all()
        print("✅ Initialized the database and created all tables.")

    # --- 5. معالجات أحداث SocketIO ---
    @socketio.on('connect')
    def on_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def on_disconnect():
        print('Client disconnected')

    return app

# --- 6. نقطة الدخول للتشغيل المباشر (للتطوير فقط) ---
if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

