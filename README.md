# Mzadd Auction Platform - مشروع مزادات إلكترونية

## الملفات الأساسية
- Backend: Flask + Flask-SocketIO
- Frontend: React + Vite (Admin Dashboard & Bidding Interface)
- قاعدة البيانات: SQLite (تجريبي), يمكن استبدالها بـ PostgreSQL للإنتاج

## خطوات التشغيل محليًا

### Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```

### Frontend
- Admin Dashboard:
```bash
cd frontend/admin-dashboard
npm install
npm run dev
```
- Bidding Interface:
```bash
cd frontend/bidding-interface
npm install
npm run dev
```

## ملاحظات
- ضع القيم الحقيقية في ملف .env المحلي (غير مرفوع للـ GitHub)
- تأكد من أن API URL في الواجهة يشير إلى http://localhost:5000 أثناء التطوير
