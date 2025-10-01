#!/bin/bash

# سكريبت تشغيل مشروع Mzadd على Kali Linux
# Mzadd Project Startup Script for Kali Linux

echo "🚀 بدء تشغيل مشروع Mzadd..."
echo "🚀 Starting Mzadd Project..."

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت. يرجى تثبيته أولاً."
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# التحقق من وجود Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js غير مثبت. يرجى تثبيته أولاً."
    echo "❌ Node.js is not installed. Please install it first."
    exit 1
fi

# التحقق من وجود pnpm
if ! command -v pnpm &> /dev/null; then
    echo "⚠️  pnpm غير مثبت. سيتم تثبيته..."
    echo "⚠️  pnpm is not installed. Installing..."
    npm install -g pnpm
fi

# الانتقال إلى مجلد المشروع
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "📁 مجلد المشروع: $PROJECT_DIR"
echo "📁 Project directory: $PROJECT_DIR"

# إعداد الخادم الخلفي
echo "🔧 إعداد الخادم الخلفي..."
echo "🔧 Setting up backend..."

cd backend

# إنشاء البيئة الافتراضية إذا لم تكن موجودة
if [ ! -d "venv" ]; then
    echo "📦 إنشاء البيئة الافتراضية..."
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تثبيت المتطلبات
echo "📦 تثبيت متطلبات Python..."
echo "📦 Installing Python requirements..."
pip install -r requirements.txt

# إنشاء ملف .env إذا لم يكن موجوداً
if [ ! -f ".env" ]; then
    echo "⚙️  إنشاء ملف البيئة..."
    echo "⚙️  Creating environment file..."
    cat > .env << EOF
SECRET_KEY=mzadd_secret_key_$(date +%s)
DATABASE_URL=sqlite:///mzadd.db
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
EOF
fi

# تهيئة قاعدة البيانات
if [ ! -f "mzadd.db" ]; then
    echo "🗄️  تهيئة قاعدة البيانات..."
    echo "🗄️  Initializing database..."
    python seed_data.py
fi

# العودة إلى المجلد الرئيسي
cd "$PROJECT_DIR"

# إعداد الواجهات الأمامية
echo "🎨 إعداد الواجهات الأمامية..."
echo "🎨 Setting up frontend applications..."

# لوحة تحكم الإدارة
echo "📊 إعداد لوحة تحكم الإدارة..."
echo "📊 Setting up admin dashboard..."
cd frontend/admin-dashboard
if [ ! -d "node_modules" ]; then
    pnpm install
fi

cd "$PROJECT_DIR"

# واجهة المزايدة
echo "🏷️  إعداد واجهة المزايدة..."
echo "🏷️  Setting up bidding interface..."
cd frontend/bidding-interface
if [ ! -d "node_modules" ]; then
    pnpm install
fi

cd "$PROJECT_DIR"

# لوحة تحكم التاجر
echo "🏪 إعداد لوحة تحكم التاجر..."
echo "🏪 Setting up merchant dashboard..."
cd frontend/merchant-dashboard
if [ ! -d "node_modules" ]; then
    pnpm install
fi

cd "$PROJECT_DIR"

echo "✅ تم إعداد جميع المكونات بنجاح!"
echo "✅ All components setup successfully!"

echo ""
echo "🚀 لتشغيل المشروع، افتح 4 terminals منفصلة وشغل الأوامر التالية:"
echo "🚀 To run the project, open 4 separate terminals and run the following commands:"
echo ""
echo "Terminal 1 - الخادم الخلفي (Backend):"
echo "cd $PROJECT_DIR/backend && source venv/bin/activate && python app.py"
echo ""
echo "Terminal 2 - لوحة تحكم الإدارة (Admin Dashboard):"
echo "cd $PROJECT_DIR/frontend/admin-dashboard && pnpm run dev"
echo ""
echo "Terminal 3 - واجهة المزايدة (Bidding Interface):"
echo "cd $PROJECT_DIR/frontend/bidding-interface && pnpm run dev"
echo ""
echo "Terminal 4 - لوحة تحكم التاجر (Merchant Dashboard):"
echo "cd $PROJECT_DIR/frontend/merchant-dashboard && pnpm run dev"
echo ""
echo "🌐 الروابط:"
echo "🌐 URLs:"
echo "- Backend API: http://localhost:5000"
echo "- Admin Dashboard: http://localhost:5173"
echo "- Bidding Interface: http://localhost:5174"
echo "- Merchant Dashboard: http://localhost:5175"
echo ""
echo "📚 للمزيد من المعلومات، راجع ملف README.md"
echo "📚 For more information, check README.md"
