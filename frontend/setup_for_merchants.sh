#!/bin/bash
set -euo pipefail

echo "🚀 بدء تحضير المشروع للنشر..."

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
# 3. تثبيت متطلبات الباكند واستبدال Eventlet بـ Gevent
# ---------------------------
echo "📦 تثبيت متطلبات الباكند..."
pip install -r backend/requirements.txt || echo "⚠️ بعض الحزم فشلت مؤقتًا"
pip install gevent Pillow==11.3.0 || true

# ---------------------------
# 4. إعداد ملفات البيئة
# ---------------------------
if [ ! -f .env ]; then
  cp env.example .env
fi
if ! grep -q "SECRET_KEY=" .env; then
  SECRET_KEY=$(openssl rand -hex 32)
  echo "SECRET_KEY=$SECRET_KEY" >> .env
  echo "🔑 تم توليد SECRET_KEY تلقائيًا"
fi

# ---------------------------
# 5. إعداد قاعدة البيانات
# ---------------------------
echo "📂 إعداد قاعدة البيانات..."
if [ -f app.db ]; then
  cp app.db app.db.bak.$(date +%Y%m%d%H%M%S)
  echo "📦 تم عمل نسخة احتياطية من قاعدة البيانات الحالية"
fi

python3 <<EOF
import sqlite3
conn = sqlite3.connect('app.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)''')
c.execute("INSERT OR IGNORE INTO users (email, username, password) VALUES (?, ?, ?)",
          ("test@example.com", "testuser", "password123"))
conn.commit()
conn.close()
EOF
echo "✅ قاعدة البيانات جاهزة."

# ---------------------------
# 6. فحص المشروع
# ---------------------------
[ -d backend ] && echo "✔️ مجلد backend موجود." || echo "❌ مجلد backend غير موجود!"
[ -d frontend ] && echo "✔️ مجلد frontend موجود." || echo "❌ مجلد frontend غير موجود!"
[ -f README.md ] && echo "✔️ README.md موجود." || echo "❌ README.md غير موجود!"

# ---------------------------
# 7. تشغيل frontend إذا موجود
# ---------------------------
if [ -f frontend/package.json ]; then
  echo "📂 تثبيت وتشغيل frontend..."
  cd frontend
  npm install
  npm run dev
  cd ..
else
  echo "⚠️ لا يوجد package.json في frontend → تم تخطي تشغيل الواجهة"
fi

echo "🎯 المشروع جاهز لاستقبال التجار."
echo "لتشغيل المشروع backend لاحقًا:"
echo "  source venv/bin/activate"
echo "  python3 backend/app.py"
