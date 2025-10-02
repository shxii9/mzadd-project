#!/bin/bash
set -euo pipefail

echo "📂 إعداد قاعدة البيانات التجريبية المحدثة..."

# عمل نسخة احتياطية إذا كانت موجودة
if [ -f app.db ]; then
  cp app.db app.db.bak.$(date +%Y%m%d%H%M%S)
  echo "📦 تم عمل نسخة احتياطية من قاعدة البيانات الحالية"
fi

# إنشاء قاعدة البيانات والجداول
python3 <<EOF
import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# إنشاء جدول المستخدمين مع الأعمدة الصحيحة
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# إدخال بيانات اختبارية بدون تكرار
test_user = ("test@example.com", "testuser", "password123")
c.execute("SELECT COUNT(*) FROM users WHERE email = ?", (test_user[0],))
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", test_user)
    print("✅ تم إضافة المستخدم الاختباري")
else:
    print("ℹ️ المستخدم الاختباري موجود بالفعل، لم يتم الإضافة")

conn.commit()
conn.close()
EOF

echo "✅ قاعدة البيانات التجريبية جاهزة!"
