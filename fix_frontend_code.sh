#!/bin/bash

echo "Starting the process to fix App.jsx in all frontend projects..."

# --- تعريف المحتوى الجديد ---
# نستخدم "Here Document" (EOF) لتعريف نص متعدد الأسطر بسهولة.
read -r -d '' NEW_CONTENT <<'EOF'
import { Button } from '@/components/ui/button.jsx'
import './App.css'

function App() {
  return (
    <>
      <div>
        <h1>مرحباً بك في لوحة التحكم</h1>
        <p>هذه هي الصفحة الرئيسية. نحن جاهزون الآن لبناء الميزات.</p>
        <Button>زر اختباري</Button>
      </div>
    </>
  )
}

export default App
EOF

# --- تحديد مسار الواجهات الأمامية ---
FRONTEND_DIR="./frontend"

# --- المرور على كل واجهة وتطبيق التعديل ---
for app_dir in "$FRONTEND_DIR"/*/; do
    if [ -d "$app_dir" ]; then
        app_name=$(basename "$app_dir")
        target_file="${app_dir}src/App.jsx"

        if [ -f "$target_file" ]; then
            echo "Fixing $target_file..."
            # نستخدم > لإعادة الكتابة فوق الملف بالكامل بالمحتوى الجديد
            echo "$NEW_CONTENT" > "$target_file"
            echo "Successfully updated $app_name."
        else
            echo "Warning: $target_file not found in $app_name."
        fi
        echo "---"
    fi
done

echo "All App.jsx files have been updated successfully!"
