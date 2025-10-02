#!/bin/bash
# سكربت لإضافة الملفات الأساسية للمشروع: .gitignore, env.example, README.md

# التأكد من التشغيل من داخل مجلد المشروع
if [ ! -d ".git" ]; then
    echo "⚠️ هذا المجلد ليس مستودع Git. شغّل السكربت داخل مجلد المشروع."
    exit 1
fi

echo "🚀 إضافة الملفات الأساسية..."

# إنشاء .gitignore
cat > .gitignore <<EOL
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.env
*.sqlite3

# Node / frontend
node_modules/
dist/
build/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store

# IDE / OS
.vscode/
.idea/
*.swp
Thumbs.db
EOL

echo ".gitignore تم إنشاؤه."

# إنشاء env.example
cat > env.example <<EOL
# متغيرات البيئة
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///app.db
VITE_API_URL=http://localhost:5000
EOL

echo "env.example تم إنشاؤه."

# إنشاء README.md مبدئي
cat > README.md <<EOL
# Mzadd Auction Platform - مشروع مزادات إلكترونية

## الملفات الأساسية
- Backend: Flask + Flask-SocketIO
- Frontend: React + Vite (Admin Dashboard & Bidding Interface)
- قاعدة البيانات: SQLite (تجريبي), يمكن استبدالها بـ PostgreSQL للإنتاج

## خطوات التشغيل محليًا

### Backend
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
\`\`\`

### Frontend
- Admin Dashboard:
\`\`\`bash
cd frontend/admin-dashboard
npm install
npm run dev
\`\`\`
- Bidding Interface:
\`\`\`bash
cd frontend/bidding-interface
npm install
npm run dev
\`\`\`

## ملاحظات
- ضع القيم الحقيقية في ملف .env المحلي (غير مرفوع للـ GitHub)
- تأكد من أن API URL في الواجهة يشير إلى http://localhost:5000 أثناء التطوير
EOL

echo "README.md تم إنشاؤه."

# Git commit
git add .gitignore env.example README.md
git commit -m "إضافة الملفات الأساسية: gitignore, env.example, README"

echo "✅ الملفات الأساسية مضافة وتم عمل commit جاهز للرفع."
