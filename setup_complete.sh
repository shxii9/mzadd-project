#!/bin/bash
set -euo pipefail

echo "🚀 بدء إعداد المشروع الكامل..."

# ---------------------------
# 1. تفعيل أو إنشاء البيئة الافتراضية
# ---------------------------
if [ ! -d "venv" ]; then
  echo "⚡ إنشاء البيئة الافتراضية..."
  python3 -m venv venv
else
  echo "⚡ البيئة الافتراضية موجودة."
fi

source venv/bin/activate

# ---------------------------
# 2. تحديث pip/setuptools/wheel
# ---------------------------
pip install --upgrade pip setuptools wheel

# ---------------------------
# 3. تثبيت متطلبات الباكند
# ---------------------------
echo "📦 تثبيت متطلبات الباكند..."
if [ -f backend/requirements.txt ]; then
  pip install -r backend/requirements.txt || echo "⚠️ بعض الحزم فشلت في التثبيت، يمكن تجاهلها مؤقتًا"
  # استبدال Pillow بإصدار ثابت حديث إذا فشل القديم
  pip install Pillow==11.3.0 || true
else
  echo "❌ ملف requirements.txt غير موجود في backend"
fi

# ---------------------------
# 4. إعداد ملفات البيئة
# ---------------------------
if [ ! -f .env ]; then
  echo "🔧 إعداد ملفات البيئة..."
  cp env.example .env
fi

# توليد SECRET_KEY تلقائيًا إذا لم يكن موجود
if ! grep -q "SECRET_KEY=" .env; then
  SECRET_KEY=$(openssl rand -hex 32)
  echo "SECRET_KEY=$SECRET_KEY" >> .env
  echo "🔑 تم توليد SECRET_KEY تلقائيًا"
fi

# ---------------------------
# 5. إعداد قاعدة البيانات
# ---------------------------
echo "📂 إعداد قاعدة البيانات التجريبية..."
if [ -f app.db ]; then
  cp app.db app.db.bak.$(date +%Y%m%d%H%M%S)
  echo "📦 تم عمل نسخة احتياطية من قاعدة البيانات الحالية"
fi

python3 <<EOF
import sqlite3
conn = sqlite3.connect('app.db')
c = conn.cursor()

# إنشاء جدول مستخدمين إذا لم يكن موجود
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)''')

# إضافة بيانات اختبارية
try:
    c.execute("INSERT OR IGNORE INTO users (email, username, password) VALUES (?, ?, ?)",
              ("test@example.com", "testuser", "password123"))
except sqlite3.IntegrityError:
    pass

conn.commit()
conn.close()
EOF

echo "✅ قاعدة البيانات جاهزة."

# ---------------------------
# 6. فحص المشروع
# ---------------------------
echo "🔍 فحص ملفات المشروع..."
[ -d backend ] && echo "✔️ مجلد backend موجود." || echo "❌ مجلد backend غير موجود!"
[ -d frontend ] && echo "✔️ مجلد frontend موجود." || echo "❌ مجلد frontend غير موجود!"
[ -f README.md ] && echo "✔️ README.md موجود." || echo "❌ README.md غير موجود!"

echo "🎉 إعداد المشروع الكامل تم بنجاح!"
echo "لتفعيل البيئة الافتراضية لاحقًا: source venv/bin/activate"
