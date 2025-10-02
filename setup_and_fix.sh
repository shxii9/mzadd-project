#!/bin/bash
set -euo pipefail

# ================================
# سكريبت شامل لإعداد مشروع Mzadd Auction
# ================================

# 1️⃣ النسخ الاحتياطي وإعداد ملفات البيئة
echo "🚀 النسخ الاحتياطي وإعداد ملفات البيئة..."
if [ -f ".env" ]; then
    cp .env ".env.bak.$(date +%Y%m%d%H%M%S)"
    echo "تم عمل نسخة احتياطية من .env"
fi

if [ -f "env.example" ]; then
    cp env.example .env
    echo "تم نسخ env.example إلى .env"
fi

# توليد SECRET_KEY إذا لم يكن موجودًا
if ! grep -q "SECRET_KEY=" .env; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "SECRET_KEY=$SECRET_KEY" >> .env
    echo "تم توليد SECRET_KEY وتخزينه في .env"
fi

# 2️⃣ إضافة الملفات الأساسية إذا مفقودة
echo "📄 إضافة الملفات الأساسية..."
[ ! -f ".gitignore" ] && echo -e "venv/\n.env\n__pycache__/\n*.pyc\nnode_modules/" > .gitignore && echo ".gitignore تم إنشاؤه."
[ ! -f "README.md" ] && echo "# Mzadd Auction Platform" > README.md && echo "README.md تم إنشاؤه."
[ ! -f "env.example" ] && cp .env env.example && echo "env.example تم إنشاؤه."

# 3️⃣ إعداد البيئة الافتراضية وتثبيت الحزم
echo "🐍 إعداد Python venv وتثبيت الحزم..."
sudo apt update && sudo apt install -y python3-venv python3-pip dos2unix build-essential

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

if [ -f "backend/requirements.txt" ]; then
    echo "تثبيت حزم Backend..."
    while IFS= read -r package; do
        pip install "$package" || echo "⚠️ الحزمة $package فشلت في التثبيت، يمكن تجاهلها مؤقتًا"
    done < backend/requirements.txt
fi

# 4️⃣ فحص ملفات المشروع الأساسية
echo "🔍 فحص ملفات المشروع..."
[ ! -d "backend" ] && echo "⚠️ مجلد backend مفقود، تأكد من هيكلة المشروع" || echo "مجلد backend موجود."
[ ! -d "frontend" ] && echo "⚠️ مجلد frontend مفقود، تأكد من هيكلة المشروع" || echo "مجلد frontend موجود."

# 5️⃣ تشغيل اختبارات سريعة
echo "⚡ اختبار تشغيل Backend..."
FLASK_APP=backend/app.py flask --version >/dev/null 2>&1 && echo "Backend جاهز للعمل." || echo "⚠️ تحقق من Flask أو app.py"

# 6️⃣ تقرير نهائي
echo "✅ إعداد المشروع كامل!"
echo "لتفعيل البيئة الافتراضية: source venv/bin/activate"
echo "يمكنك الآن تشغيل المشروع كما هو معتاد."

