#!/bin/bash
set -euo pipefail

# ================================
# سكريبت لإعداد قاعدة البيانات للاختبار
# ================================

# تفعيل البيئة الافتراضية
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ البيئة الافتراضية غير موجودة. شغّل setup_and_fix.sh أولاً."
    exit 1
fi

# التحقق من وجود ملف قاعدة البيانات
DB_FILE="app.db"
if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "${DB_FILE}.bak.$(date +%Y%m%d%H%M%S)"
    echo "تم عمل نسخة احتياطية من قاعدة البيانات الحالية."
fi

# إنشاء قاعدة بيانات جديدة فارغة
echo "📂 إنشاء قاعدة بيانات جديدة..."
python3 <<EOF
import sqlite3

conn = sqlite3.connect('$DB_FILE')
c = conn.cursor()

# إنشاء جدول مستخدمين كمثال
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# إضافة بعض بيانات الاختبار
users = [
    ('alice', 'alice@example.com', 'hashed_password_1'),
    ('bob', 'bob@example.com', 'hashed_password_2'),
    ('charlie', 'charlie@example.com', 'hashed_password_3')
]
c.executemany('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', users)

conn.commit()
conn.close()
print("✅ قاعدة البيانات جاهزة للاختبار مع بيانات المستخدمين.")
EOF
