#!/bin/bash

# عنوان الواجهة الخلفية
API_URL="VITE_API_URL=http://127.0.0.1:5000"

# المسار إلى مجلد الواجهات الأمامية
FRONTEND_DIR="./frontend"

echo "Starting setup for all frontend applications..."

# المرور على كل مجلد داخل frontend
for app_dir in "$FRONTEND_DIR"/*/; do
    if [ -d "$app_dir" ]; then
        app_name=$(basename "$app_dir" )
        echo "--- Setting up $app_name ---"

        # 1. إنشاء ملف .env
        if [ ! -f "$app_dir/.env" ]; then
            echo "$API_URL" > "$app_dir/.env"
            echo ".env file created for $app_name."
        else
            echo ".env file already exists for $app_name."
        fi

        # 2. تثبيت الاعتماديات مع حل مشكلة التعارض
        echo "Installing dependencies for $app_name..."
        # --- هذا هو السطر الذي تم تعديله ---
        (cd "$app_dir" && npm install --legacy-peer-deps)
        
        echo "--- Finished setup for $app_name ---"
        echo ""
    fi
done

echo "All frontend applications have been configured successfully!"

