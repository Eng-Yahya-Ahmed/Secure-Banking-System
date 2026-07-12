# استخدام نسخة خفيفة من Python 3.12
FROM python:3.12-slim

# منع Python من إنشاء ملفات pycache
ENV PYTHONDONTWRITEBYTECODE=1

# إظهار رسائل Python وFlask مباشرة في Terminal
ENV PYTHONUNBUFFERED=1

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المكتبات أولًا
COPY backend/requirements.txt ./requirements.txt

# تحديث pip وتثبيت مكتبات المشروع
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات Backend إلى الحاوية
COPY backend/ .

# توضيح أن التطبيق يعمل على المنفذ 5000
EXPOSE 5000

# الأمر الذي يعمل عند تشغيل الحاوية
CMD ["python", "run.py"]