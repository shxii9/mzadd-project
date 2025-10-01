# مرحلة البناء
FROM node:18-alpine AS build

WORKDIR /app

# نسخ ملفات package.json و pnpm-lock.yaml
COPY package.json pnpm-lock.yaml* ./

# تثبيت pnpm
RUN npm install -g pnpm

# تثبيت الاعتماديات
RUN pnpm install

# نسخ باقي ملفات التطبيق
COPY . .

# بناء التطبيق للإنتاج
RUN pnpm run build

# مرحلة الإنتاج
FROM nginx:stable-alpine

# نسخ الملفات المبنية من مرحلة البناء
COPY --from=build /app/dist /usr/share/nginx/html

# كشف المنفذ
EXPOSE 80

# تشغيل Nginx
CMD ["nginx", "-g", "daemon off;"]
