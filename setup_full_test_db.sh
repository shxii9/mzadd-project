#!/bin/bash
set -euo pipefail

# ================================
# سكريبت إعداد قاعدة بيانات اختبارية متكاملة
# ================================

DB_FILE="app.db"

# تفعيل البيئة الافتراضية
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ البيئة الافتراضية غير موجودة. شغّل setup_and_fix.sh أولاً."
    exit 1
fi

# النسخ الاحتياطي إذا كانت قاعدة البيانات موجودة
if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "${DB_FILE}.bak.$(date +%Y%m%d%H%M%S)"
    echo "تم عمل نسخة احتياطية من قاعدة البيانات الحالية."
fi

# إنشاء قاعدة بيانات جديدة وملئها بالبيانات التجريبية
python3 <<EOF
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('$DB_FILE')
c = conn.cursor()

# إنشاء الجداول الأساسية
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS auctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    auction_id INTEGER NOT NULL,
    FOREIGN KEY(auction_id) REFERENCES auctions(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    user_id INTEGER NOT NULL,
    auction_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(auction_id) REFERENCES auctions(id)
)
''')

# إضافة بيانات تجريبية
users = [
    ('alice', 'alice@example.com', 'hashed_password_1'),
    ('bob', 'bob@example.com', 'hashed_password_2'),
    ('charlie', 'charlie@example.com', 'hashed_password_3')
]
c.executemany('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', users)

# إنشاء مزادات مرتبطة بالمستخدمين
auctions = [
    ('مزاد الإلكترونيات', 'بيع أجهزة إلكترونية مستعملة', datetime.now().isoformat(), (datetime.now() + timedelta(days=7)).isoformat(), 1),
    ('مزاد الكتب', 'بيع كتب قديمة ونادرة', datetime.now().isoformat(), (datetime.now() + timedelta(days=5)).isoformat(), 2)
]
c.executemany('INSERT INTO auctions (title, description, start_time, end_time, owner_id) VALUES (?, ?, ?, ?, ?)', auctions)

# إضافة عناصر للمزادات
items = [
    ('لابتوب قديم', 'جهاز لابتوب مستعمل بحالة جيدة', 1),
    ('هاتف ذكي', 'هاتف ذكي مستعمل', 1),
    ('كتاب نادر', 'نسخة قديمة من كتاب مشهور', 2)
]
c.executemany('INSERT INTO items (name, description, auction_id) VALUES (?, ?, ?)', items)

# إضافة عروض (bids)
bids = [
    (150.0, 2, 1, datetime.now().isoformat()),
    (200.0, 3, 1, datetime.now().isoformat()),
    (50.0, 1, 2, datetime.now().isoformat())
]
c.executemany('INSERT INTO bids (amount, user_id, auction_id, created_at) VALUES (?, ?, ?, ?)', bids)

conn.commit()
conn.close()
print("✅ قاعدة البيانات التجريبية المتقدمة جاهزة مع جميع الجداول والبيانات.")
EOF
