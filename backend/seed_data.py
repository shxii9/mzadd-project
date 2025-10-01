"""
Seed Data Script for Mzadd Auction Platform
Populates the database with realistic sample data for Kuwait market
"""

import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from models_enhanced import (
    db, User, Item, Auction, Bid, Notification,
    UserRole, ItemStatus, AuctionStatus
)
import json

# Kuwait-specific sample data
KUWAITI_NAMES = [
    "أحمد محمد الكندري", "فاطمة علي العتيبي", "خالد سعد المطيري", "نورا أحمد الرشيد",
    "محمد خالد الصباح", "سارة عبدالله الخالد", "عبدالله يوسف العنزي", "مريم حمد الهاجري",
    "سعد محمد البدر", "هند علي الشمري", "يوسف أحمد القطامي", "لطيفة سالم العجمي",
    "حمد عبدالله الثاني", "عائشة محمد الفهد", "طلال سعد الصقر", "شيخة يوسف المبارك"
]

USERNAMES = [
    "ahmed_kw", "fatima_kuwait", "khalid_store", "nora_auctions",
    "mohammed_deals", "sara_collector", "abdullah_trader", "maryam_vintage",
    "saad_electronics", "hind_jewelry", "youssef_cars", "lateefa_fashion",
    "hamad_antiques", "aisha_books", "talal_watches", "sheikha_art"
]

ITEM_CATEGORIES = {
    "إلكترونيات": [
        "آيفون 15 برو ماكس 256 جيجا", "سامسونج جالاكسي S24 الترا", "آيباد برو 12.9 إنش",
        "ماك بوك برو M3", "بلايستيشن 5", "إكس بوكس سيريس X", "نينتندو سويتش OLED",
        "كاميرا كانون EOS R5", "درون DJI Mini 4 Pro", "ساعة آبل الترا 2"
    ],
    "مجوهرات": [
        "ساعة رولكس سابمارينر", "خاتم ذهب عيار 21", "عقد لؤلؤ طبيعي", "أساور ذهب نسائية",
        "ساعة أوميجا سبيدماستر", "خاتم ألماس 2 قيراط", "طقم ذهب كامل", "ساعة كارتييه نسائية",
        "عقد ذهب بالأحجار الكريمة", "أقراط ألماس"
    ],
    "سيارات": [
        "تويوتا كامري 2023", "لكزس ES 350", "مرسيدس بنز C-Class", "بي إم دبليو X5",
        "أودي A6", "نيسان باترول", "فورد موستانج", "شيفروليه تاهو", "جيب رانجلر", "هوندا أكورد"
    ],
    "أثاث": [
        "طقم صالة كلاسيكي", "غرفة نوم مودرن", "طاولة طعام خشبية", "كنبة جلد إيطالية",
        "خزانة ملابس كبيرة", "مكتب مكتبي فاخر", "كراسي طعام مبطنة", "طاولة قهوة رخامية",
        "مكتبة خشبية", "سرير أطفال"
    ],
    "أزياء": [
        "حقيبة لويس فيتون", "حذاء لوبوتان", "ساعة شانيل", "عباءة مطرزة", "ثوب رجالي فاخر",
        "حقيبة هيرمس بيركين", "حذاء غوتشي", "نظارة برادا", "وشاح هيرمس", "حقيبة ديور"
    ],
    "مقتنيات": [
        "طوابع كويتية نادرة", "عملات قديمة", "لوحة فنية أصلية", "كتاب نادر", "تحفة أثرية",
        "ساعة جيب عتيقة", "خنجر كويتي تراثي", "مخطوطة قديمة", "تحفة فضية", "قطعة تراثية"
    ]
}

def create_sample_users():
    """Create sample users with different roles"""
    users = []
    
    # Create admin user
    admin = User(
        username='admin_mzadd',
        email='admin@mzadd.com',
        role=UserRole.ADMIN,
        first_name='مدير',
        last_name='النظام',
        phone='+965 9999 0000',
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow() - timedelta(days=365),
        last_login=datetime.utcnow(),
        login_count=150
    )
    admin.set_password('admin123')
    users.append(admin)
    
    # Create merchants and bidders
    for i, (name, username) in enumerate(zip(KUWAITI_NAMES, USERNAMES)):
        # First 8 are merchants, rest are bidders
        role = UserRole.MERCHANT if i < 8 else UserRole.BIDDER
        
        user = User(
            username=username,
            email=f'{username}@example.com',
            role=role,
            full_name=name,
            first_name=name.split()[0],
            last_name=' '.join(name.split()[1:]),
            phone=f'+965 {random.randint(5000, 9999)} {random.randint(1000, 9999)}',
            is_active=True,
            is_verified=random.choice([True, True, True, False]),  # 75% verified
            created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            last_login=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            login_count=random.randint(5, 100),
            commission_rate=random.uniform(0.03, 0.07) if role == UserRole.MERCHANT else 0.05,
            total_earnings=random.uniform(100, 5000) if role == UserRole.MERCHANT else 0
        )
        user.set_password('password123')
        users.append(user)
    
    return users

def create_sample_items(merchants):
    """Create sample items for merchants"""
    items = []
    
    for merchant in merchants:
        # Each merchant has 3-8 items
        num_items = random.randint(3, 8)
        
        for _ in range(num_items):
            category = random.choice(list(ITEM_CATEGORIES.keys()))
            item_name = random.choice(ITEM_CATEGORIES[category])
            
            # Generate realistic prices based on category
            price_ranges = {
                "إلكترونيات": (200, 2000),
                "مجوهرات": (500, 5000),
                "سيارات": (8000, 25000),
                "أثاث": (100, 1500),
                "أزياء": (150, 3000),
                "مقتنيات": (50, 2000)
            }
            
            min_price, max_price = price_ranges[category]
            start_price = random.uniform(min_price, max_price)
            reserve_price = start_price * random.uniform(1.1, 1.5) if random.choice([True, False]) else None
            
            item = Item(
                name=item_name,
                description=f"وصف تفصيلي لـ {item_name}. سلعة أصلية وبحالة ممتازة.",
                category=category,
                start_price=start_price,
                reserve_price=reserve_price,
                status=random.choice([ItemStatus.ACTIVE, ItemStatus.ACTIVE, ItemStatus.PENDING]),
                owner_id=merchant.id,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                image_url=f"/images/{category.lower()}/{random.randint(1, 10)}.jpg",
                additional_images=[
                    f"/images/{category.lower()}/{random.randint(11, 20)}.jpg",
                    f"/images/{category.lower()}/{random.randint(21, 30)}.jpg"
                ]
            )
            items.append(item)
    
    return items

def create_sample_auctions(items):
    """Create sample auctions for items"""
    auctions = []
    
    for item in items:
        if item.status != ItemStatus.ACTIVE:
            continue
            
        # 70% chance of having an auction
        if random.random() < 0.7:
            now = datetime.utcnow()
            
            # Determine auction timing
            auction_type = random.choice(['active', 'scheduled', 'ended'])
            
            if auction_type == 'active':
                start_time = now - timedelta(hours=random.randint(1, 48))
                end_time = now + timedelta(hours=random.randint(1, 72))
                status = AuctionStatus.ACTIVE
            elif auction_type == 'scheduled':
                start_time = now + timedelta(hours=random.randint(1, 168))
                end_time = start_time + timedelta(hours=random.randint(24, 168))
                status = AuctionStatus.SCHEDULED
            else:  # ended
                start_time = now - timedelta(hours=random.randint(48, 336))
                end_time = start_time + timedelta(hours=random.randint(24, 168))
                status = AuctionStatus.CLOSED
            
            auction = Auction(
                item_id=item.id,
                start_time=start_time,
                end_time=end_time,
                current_price=item.start_price,
                status=status,
                total_bids=0,
                unique_bidders=0,
                created_at=start_time - timedelta(hours=random.randint(1, 24))
            )
            auctions.append(auction)
    
    return auctions

def create_sample_bids(auctions, bidders):
    """Create sample bids for auctions"""
    bids = []
    
    for auction in auctions:
        if auction.status == AuctionStatus.SCHEDULED:
            continue
            
        # Generate 0-25 bids per auction
        num_bids = random.randint(0, 25)
        current_price = auction.current_price
        
        bid_times = []
        for _ in range(num_bids):
            # Bids are distributed throughout the auction period
            bid_time = auction.start_time + timedelta(
                seconds=random.randint(0, int((auction.end_time - auction.start_time).total_seconds()))
            )
            bid_times.append(bid_time)
        
        bid_times.sort()
        unique_bidders_set = set()
        
        for i, bid_time in enumerate(bid_times):
            bidder = random.choice(bidders)
            
            # Increment price by 5-50 KWD
            increment = random.uniform(5, 50)
            current_price += increment
            
            bid = Bid(
                auction_id=auction.id,
                bidder_id=bidder.id,
                amount=current_price,
                timestamp=bid_time,
                is_valid=True
            )
            bids.append(bid)
            unique_bidders_set.add(bidder.id)
        
        # Update auction with final stats
        auction.current_price = current_price
        auction.total_bids = len(bids)
        auction.unique_bidders = len(unique_bidders_set)
        
        if bids and auction.status == AuctionStatus.CLOSED:
            auction.winning_bid_id = bids[-1].id  # Last bid wins
    
    return bids

def create_sample_notifications(users, auctions):
    """Create sample notifications for users"""
    notifications = []
    
    notification_templates = [
        {
            'title': 'مزاد جديد',
            'message': 'تم إنشاء مزاد جديد في فئة {category}',
            'type': 'auction'
        },
        {
            'title': 'تم تجاوز مزايدتك',
            'message': 'تم تجاوز مزايدتك في المزاد "{item_name}"',
            'type': 'bid'
        },
        {
            'title': 'انتهى المزاد',
            'message': 'انتهى المزاد "{item_name}" - تحقق من النتائج',
            'type': 'auction'
        },
        {
            'title': 'مبروك!',
            'message': 'لقد ربحت المزاد "{item_name}"',
            'type': 'system'
        }
    ]
    
    for user in users:
        if user.role == UserRole.ADMIN:
            continue
            
        # Generate 3-10 notifications per user
        num_notifications = random.randint(3, 10)
        
        for _ in range(num_notifications):
            template = random.choice(notification_templates)
            auction = random.choice(auctions)
            
            notification = Notification(
                user_id=user.id,
                title=template['title'],
                message=template['message'].format(
                    category=auction.item.category,
                    item_name=auction.item.name
                ),
                type=template['type'],
                is_read=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                auction_id=auction.id,
                item_id=auction.item_id
            )
            notifications.append(notification)
    
    return notifications

def seed_database():
    """Main function to seed the database with sample data"""
    print("🌱 Starting database seeding...")
    
    try:
        # Clear existing data (be careful in production!)
        print("Clearing existing data...")
        db.session.query(Notification).delete()
        db.session.query(Bid).delete()
        db.session.query(Auction).delete()
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create users
        print("Creating users...")
        users = create_sample_users()
        db.session.add_all(users)
        db.session.commit()
        
        merchants = [u for u in users if u.role == UserRole.MERCHANT]
        bidders = [u for u in users if u.role == UserRole.BIDDER]
        
        print(f"Created {len(users)} users ({len(merchants)} merchants, {len(bidders)} bidders)")
        
        # Create items
        print("Creating items...")
        items = create_sample_items(merchants)
        db.session.add_all(items)
        db.session.commit()
        
        print(f"Created {len(items)} items")
        
        # Create auctions
        print("Creating auctions...")
        auctions = create_sample_auctions(items)
        db.session.add_all(auctions)
        db.session.commit()
        
        active_auctions = [a for a in auctions if a.status == AuctionStatus.ACTIVE]
        print(f"Created {len(auctions)} auctions ({len(active_auctions)} active)")
        
        # Create bids
        print("Creating bids...")
        bids = create_sample_bids(auctions, bidders)
        db.session.add_all(bids)
        db.session.commit()
        
        print(f"Created {len(bids)} bids")
        
        # Create notifications
        print("Creating notifications...")
        notifications = create_sample_notifications(users, auctions)
        db.session.add_all(notifications)
        db.session.commit()
        
        print(f"Created {len(notifications)} notifications")
        
        print("✅ Database seeding completed successfully!")
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"- Users: {len(users)} (1 admin, {len(merchants)} merchants, {len(bidders)} bidders)")
        print(f"- Items: {len(items)}")
        print(f"- Auctions: {len(auctions)} ({len(active_auctions)} active)")
        print(f"- Bids: {len(bids)}")
        print(f"- Notifications: {len(notifications)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.session.rollback()
        return False

if __name__ == '__main__':
    # This would be run with the Flask app context
    seed_database()
