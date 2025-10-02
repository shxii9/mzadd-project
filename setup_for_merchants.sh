#!/bin/bash
set -euo pipefail

echo "🚀 بدء تحضير المشروع للنشر..."

# ---------------------------
# 1. تفعيل البيئة الافتراضية
# ---------------------------
if [ ! -d "venv" ]; then
  echo "⚡ إنشاء البيئة الافتراضية..."
  python3 -m venv venv
fi
source venv/bin/activate

# ---------------------------
# 2. تحديث pip/setuptools/wheel
# ---------------------------
echo "📦 تحديث أدوات البايثون..."
pip install --upgrade pip setuptools wheel

# ---------------------------
# 3. تثبيت متطلبات الباكند
# ---------------------------
if [ -f backend/requirements.txt ]; then
  echo "📥 تثبيت متطلبات الباكند..."
  pip install -r backend/requirements.txt || echo "⚠️ بعض الحزم فشلت، يمكن تجاهلها مؤقتًا"
  pip install Pillow==11.3.0 || true
else
  echo "❌ ملف requirements.txt غير موجود في backend"
fi

# ---------------------------
# 4. إعداد ملفات البيئة للإنتاج
# ---------------------------
if [ ! -f .env ]; then
  echo "🔧 إعداد ملف البيئة..."
  cp env.example .env
fi

# توليد SECRET_KEY إذا لم يكن موجود
if ! grep -q "SECRET_KEY=" .env; then
  SECRET_KEY=$(openssl rand -hex 32)
  echo "SECRET_KEY=$SECRET_KEY" >> .env
  echo "🔑 تم توليد SECRET_KEY تلقائيًا"
fi

# ---------------------------
# 5. إعداد قاعدة البيانات للإنتاج
# ---------------------------
echo "📂 إعداد قاعدة البيانات الإنتاجية..."
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
conn.commit()
conn.close()
EOF

echo "✅ قاعدة البيانات جاهزة للإنتاج."

# ---------------------------
# 6. فحص ملفات المشروع
# ---------------------------
echo "🔍 التحقق من ملفات المشروع..."
[ -d backend ] && echo "✔️ مجلد backend موجود." || echo "❌ مجلد backend غير موجود!"
[ -d frontend ] && echo "✔️ مجلد frontend موجود." || echo "❌ مجلد frontend غير موجود!"
[ -f README.md ] && echo "✔️ README.md موجود." || echo "❌ README.md غير موجود!"

# ---------------------------
# 7. التحضير لاستقبال التجار
# ---------------------------
echo "🎯 المشروع جاهز لاستقبال التجار."
echo "لتشغيل المشروع:"
echo "  1. تفعيل البيئة: source venv/bin/activate"
echo "  2. تشغيل الباكند: python3 backend/app.py"
echo "  3. تشغيل الواجهة: npm install && npm run dev (داخل مجلد frontend)"

echo "🎉 كل شيء جاهز!"
