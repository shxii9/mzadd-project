# دليل تشغيل مشروع Mzadd على Kali Linux

## نظرة عامة
مشروع **Mzadd** هو منصة مزادات إلكترونية متكاملة تتكون من:
- خادم خلفي مبني بـ **Flask** (Python)
- ثلاث واجهات أمامية مبنية بـ **React**:
  - لوحة تحكم الإدارة
  - واجهة المزايدة للمستخدمين
  - لوحة تحكم التاجر

## التثبيت السريع على Kali Linux

### 1. استنساخ المشروع
```bash
git clone https://github.com/shxii9/mzadd-auction-platform.git
cd mzadd-auction-platform
```

### 2. تثبيت المتطلبات الأساسية
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و Node.js
sudo apt install -y python3 python3-pip python3-venv nodejs npm

# تثبيت pnpm
npm install -g pnpm
```

### 3. إعداد الخادم الخلفي
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# إنشاء ملف البيئة
echo "SECRET_KEY=your_secret_key_$(date +%s)
DATABASE_URL=sqlite:///mzadd.db
FLASK_APP=app.py
FLASK_ENV=development" > .env

# تهيئة قاعدة البيانات
python seed_data.py
```

### 4. تشغيل الخادم الخلفي
```bash
python app.py
```
الخادم سيعمل على: http://localhost:5000

### 5. إعداد الواجهات الأمامية (في terminals منفصلة)

#### لوحة تحكم الإدارة
```bash
cd frontend/admin-dashboard
pnpm install
pnpm run dev
```
ستعمل على: http://localhost:5173

#### واجهة المزايدة
```bash
cd frontend/bidding-interface
pnpm install
pnpm run dev
```
ستعمل على: http://localhost:5174

#### لوحة تحكم التاجر
```bash
cd frontend/merchant-dashboard
pnpm install
pnpm run dev
```
ستعمل على: http://localhost:5175

## الميزات الرئيسية
- ✅ مزايدات لحظية باستخدام WebSockets
- ✅ دعم اللغتين العربية والإنجليزية
- ✅ نظام إدارة شامل للمستخدمين والمزادات
- ✅ واجهات منفصلة للمديرين والتجار والمزايدين
- ✅ نظام عمولات وإدارة الإيرادات
- ✅ تصميم عصري وسريع الاستجابة

## استكشاف الأخطاء
للحصول على دليل مفصل لاستكشاف الأخطاء وحلها، راجع الملف الكامل للتوثيق.

## المساهمة
نرحب بالمساهمات! يرجى إنشاء Pull Request أو فتح Issue للمناقشة.

## الترخيص
MIT License - انظر ملف LICENSE للتفاصيل.
