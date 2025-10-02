#!/bin/bash
set -euo pipefail

echo "🚀 تشغيل المشروع الكامل..."

# ---------------------------
# 1. تفعيل البيئة الافتراضية للـ Python
# ---------------------------
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "⚡ تم تفعيل البيئة الافتراضية"
else
    echo "❌ البيئة الافتراضية غير موجودة! شغّل setup_full.sh أولاً"
    exit 1
fi

# ---------------------------
# 2. تشغيل Backend
# ---------------------------
echo "📦 تشغيل Backend..."
(cd backend && export FLASK_APP=app.py && flask run &)   # & لتشغيله في الخلفية

# ---------------------------
# 3. تشغيل Frontend كل جزء في الخلفية
# ---------------------------
for frontend_dir in frontend/admin-dashboard frontend/bidding-interface frontend/merchant-dashboard; do
    if [ -d "$frontend_dir" ]; then
        echo "📂 تشغيل $frontend_dir..."
        (cd "$frontend_dir" && npm install && npm start &)  # & لتشغيل كل واجهة في الخلفية
    else
        echo "❌ $frontend_dir غير موجود!"
    fi
done

echo "🎉 جميع أجزاء المشروع تعمل الآن!"
echo "⚠️ ستظل العمليات تعمل في الخلفية، اضغط Ctrl+C لإيقافها جميعًا"
wait
