#!/bin/bash
echo "Fixing all relative imports in the backend..."
# ابحث عن جميع ملفات .py داخل مجلد backend
find backend -name "*.py" -print0 | while IFS= read -r -d $'\0' file; do
    echo "Processing $file..."
    # استخدم sed لإزالة "from ." واستبدالها بـ "from "
    # ولإزالة "from .." واستبدالها بـ "from "
    sed -i 's/^from \./from /g' "$file"
    sed -i 's/^from \.\./from /g' "$file"
done
echo "All backend imports have been fixed."
