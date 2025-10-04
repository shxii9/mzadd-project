# backend/seed_data.py
from app import create_app
from models_enhanced import db, User, UserRole, Item, Auction

def create_sample_users():
    users = []
    admin = User(
        username='admin_mzadd', email='admin@mzadd.com', role=UserRole.ADMIN,
        first_name='مدير', last_name='النظام', is_active=True, is_verified=True
    )
    admin.set_password('admin123')
    users.append(admin)
    return users

def seed_database():
    print("🌱 Starting database seeding...")
    try:
        print("Clearing existing data...")
        db.session.query(Auction).delete()
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        print("Creating users...")
        users = create_sample_users()
        db.session.add_all(users)
        db.session.commit()
        
        print("✅ Database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.session.rollback()

def main():
    app = create_app()
    with app.app_context():
        print("Application context pushed.")
        seed_database()

if __name__ == '__main__':
    main()
