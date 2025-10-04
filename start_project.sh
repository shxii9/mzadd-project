#!/bin/bash

echo "Starting the Mzadd Project..."
echo "This will open multiple terminal windows for each service."

# المسار إلى المجلد الجذر للمشروع باستخدام متغير HOME
PROJECT_DIR="$HOME/mzadd-final-try"

# تشغيل الواجهة الخلفية باستخدام x-terminal-emulator
echo "Starting Backend..."
x-terminal-emulator -e "bash -c 'echo --- Backend Server ---; cd $PROJECT_DIR && source venv/bin/activate; python -m backend.app; exec bash'"

# الانتظار قليلاً لضمان بدء الواجهة الخلفية
sleep 3

# تشغيل الواجهات الأمامية
FRONTEND_DIR="$PROJECT_DIR/frontend"
for app_dir in $FRONTEND_DIR/*/; do
    if [ -d "$app_dir" ]; then
        app_name=$(basename "$app_dir")
        echo "Starting $app_name..."
        x-terminal-emulator -e "bash -c 'echo --- $app_name Frontend ---; cd $app_dir && npm run dev; exec bash'"
    fi
done

echo "All components of the Mzadd Project have been launched in new terminals."
