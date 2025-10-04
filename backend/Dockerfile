# --- المرحلة الأولى: بناء البيئة (Builder Stage) ---
FROM python:3.11-slim-bullseye AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- المرحلة الثانية: الصورة النهائية (Final Stage) ---
FROM python:3.11-slim-bullseye
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# --- تثبيت تطبيقنا كحزمة ---
# ننسخ كل شيء أولاً
COPY . .
# نثبت المشروع في وضع قابل للتعديل. هذا يحل جميع مشاكل الاستيراد.
RUN pip install -e .

RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
# هذا الأمر سيعمل الآن بشكل صحيح لأن التطبيق مثبت كحزمة
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
