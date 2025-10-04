# --- المرحلة الأولى: بناء التطبيق (Builder Stage) ---
# نستخدم صورة Node.js رسمية (إصدار 20) كنقطة بداية.
# "alpine" هي نسخة خفيفة جدًا من لينكس، مثالية لتقليل حجم الصورة.
FROM node:20-alpine AS builder

# نحدد مجلد العمل داخل الحاوية.
WORKDIR /app

# ننسخ ملفات package.json و package-lock.json أولاً.
# هذا يستفيد من التخزين المؤقت لـ Docker. طالما لم تتغير هذه الملفات،
# لن يتم إعادة تنفيذ "npm install" في كل مرة.
COPY package.json package-lock.json* ./

# نثبت الاعتماديات. نستخدم --legacy-peer-deps الذي احتجناه سابقًا.
RUN npm install --legacy-peer-deps

# ننسخ باقي كود التطبيق.
COPY . .

# نقوم ببناء التطبيق للإنتاج. هذا الأمر سيقوم بإنشاء نسخة مُصغّرة
# ومُحسّنة من التطبيق داخل مجلد /app/dist.
RUN npm run build


# --- المرحلة الثانية: الصورة النهائية (Final Stage) ---
# نبدأ من جديد بصورة خادم ويب خفيفة جدًا (Nginx).
# Nginx هو خادم ويب عالي الأداء ومثالي لتقديم الملفات الثابتة (HTML, CSS, JS)
# التي ينتجها أمر "npm run build".
FROM nginx:1.25-alpine

# ننسخ ملفات التطبيق المبنية من مرحلة البناء إلى المجلد
# الذي يقدم منه Nginx الملفات بشكل افتراضي.
COPY --from=builder /app/dist /usr/share/nginx/html

# نكشف عن المنفذ 80، وهو المنفذ الافتراضي الذي يعمل عليه Nginx.
EXPOSE 80

# الأمر الافتراضي لتشغيل Nginx.
CMD ["nginx", "-g", "daemon off;"]

