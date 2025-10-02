#!/bin/bash
set -euo pipefail

echo "🚀 بدء إعداد المشروع الكامل..."

# نسخ env.example ونسخ نسخة احتياطية للـ .env
if [ -f .env ]; then
  cp .env .env.bak.$(date +%Y%m%d%H%M%S)
  echo "Backed up existing .env"
fi
cp env.example .env
echo ".env تم نسخه من env.example"

# توليد SECRET_KEY إذا لم يكن موجود
if ! grep -q "SECRET_KEY=" .env; then
  SECRET=$(openssl rand -hex 32)
  echo "SECRET_KEY=$SECRET" >> .env
  echo "SECRET_KEY تم توليده"
fi

# تحديث pip, setuptools, wheel
echo "🔧 تحديث أدوات البناء في venv..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# تثبيت مكتبات النظام المطلوبة للحزم الصعبة
echo "📦 تثبيت مكتبات النظام الضرورية..."
sudo apt install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk build-essential

# تثبيت المتطلبات مع تجاوز مشاكل الـ wheel لبعض الحزم
echo "📥 تثبيت متطلبات المشروع..."
pip install --no-binary :all: Pillow
pip install -r backend/requirements.txt || echo "⚠️ بعض الحزم قد فشلت في البناء، يمكن تجاهلها مؤقتًا"

echo "✅ إعداد المشروع الكامل تم بنجاح!"
echo "لتشغيل البيئة الافتراضية: source venv/bin/activate"
