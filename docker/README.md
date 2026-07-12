# تشغيل النظام المصرفي الآمن باستخدام Docker

## 1. مقدمة

يوضح هذا الملف طريقة بناء وتشغيل مشروع النظام المصرفي الآمن باستخدام Docker.

يساعد Docker على تشغيل المشروع داخل بيئة مستقلة تحتوي على:

- Python 3.12.
- مكتبات Flask.
- ملفات Backend.
- إعدادات التشغيل.
- قاعدة بيانات SQLite مرتبطة بالجهاز.

---

## 2. الملفات المستخدمة

يحتوي مجلد Docker على الملفات التالية:

docker/
├── Dockerfile
├── docker-compose.yml
└── README.md
### Dockerfile

يحدد طريقة بناء صورة المشروع، مثل:

- إصدار Python.
- تثبيت المكتبات.
- نسخ ملفات Backend.
- فتح المنفذ 5000.
- تشغيل run.py.

### docker-compose.yml

يحدد طريقة تشغيل الحاوية، مثل:

- اسم الخدمة.
- مكان Dockerfile.
- ربط المنفذ 5000.
- ربط مجلد قاعدة البيانات.
- إعدادات التشغيل.

### .dockerignore

يوجد هذا الملف في المجلد الرئيسي للمشروع، ويمنع Docker من نسخ الملفات غير الضرورية أو الحساسة.

---

## 3. المتطلبات

يجب تثبيت:

Docker Desktop
ثم التأكد من أنه يعمل قبل تنفيذ الأوامر.

يمكن التحقق من Docker باستخدام:

docker --version
والتحقق من Docker Compose باستخدام:

docker compose version
---

## 4. بناء وتشغيل المشروع

افتح Terminal داخل المجلد الرئيسي:

secure_Banking_System_pro
ثم نفّذ:

docker compose -f docker/docker-compose.yml up --build
يقوم الأمر بالآتي:

1. قراءة Dockerfile.
2. تنزيل صورة Python عند الحاجة.
3. تثبيت مكتبات المشروع.
4. نسخ ملفات Backend.
5. إنشاء الحاوية.
6. تشغيل Flask على المنفذ 5000.

---

## 5. فتح النظام

بعد نجاح التشغيل افتح المتصفح على:

http://localhost:5000
أو:

http://127.0.0.1:5000
---

## 6. قاعدة البيانات

يربط Docker المجلد:

backend/instance/
بالمجلد الموجود داخل الحاوية:

/app/instance/
يساعد ذلك على الاحتفاظ بقاعدة البيانات حتى بعد إيقاف أو حذف الحاوية.

---

## 7. إيقاف المشروع

لإيقاف التشغيل مؤقتًا اضغط داخل Terminal:

Ctrl + C
ثم نفّذ:

docker compose -f docker/docker-compose.yml down
---

## 8. تشغيل المشروع مرة أخرى

بعد بناء الصورة للمرة الأولى، يمكن تشغيله باستخدام:

docker compose -f docker/docker-compose.yml up
ولتشغيله في الخلفية:

docker compose -f docker/docker-compose.yml up -d
---

## 9. مشاهدة سجلات التشغيل

لمشاهدة رسائل Flask والحاوية:

docker compose -f docker/docker-compose.yml logs
ولمتابعة الرسائل مباشرة:

docker compose -f docker/docker-compose.yml logs -f
---

## 10. عرض الحاويات العاملة

docker ps
يجب أن تظهر حاوية باسم:

secure-banking-system
---

## 11. إعادة بناء المشروع

بعد تعديل المكتبات أو Dockerfile استخدم:

docker compose -f docker/docker-compose.yml up --build
---

## 12. حذف الحاوية والصورة

لإيقاف وحذف الحاوية:

docker compose -f docker/docker-compose.yml down
لحذف الصورة أيضًا:

docker compose -f docker/docker-compose.yml down --rmi local
لا يحذف ذلك قاعدة البيانات المرتبطة داخل:

backend/instance/
---

## 13. حل المشكلات الشائعة

### Docker لا يعمل

تأكد من تشغيل Docker Desktop.

### المنفذ 5000 مستخدم

أوقف البرنامج الذي يستخدم المنفذ، أو غيّر الربط داخل docker-compose.yml مثل:

ports:
  - "5001:5000"
ثم افتح:

http://localhost:5001
### مكتبة Python غير موجودة

تأكد من إضافتها إلى:

backend/requirements.txt
ثم أعد البناء:

docker compose -f docker/docker-compose.yml up --build
### التطبيق لا يفتح

شاهد السجلات:

docker compose -f docker/docker-compose.yml logs -f
### التغييرات لا تظهر

أعد بناء الصورة:

docker compose -f docker/docker-compose.yml up --build
---

## 14. ملاحظات أمنية

- لا تضع كلمات المرور داخل Dockerfile.
- لا ترفع ملف .env إلى GitHub.
- لا ترفع قاعدة البيانات الحقيقية.
- لا تستخدم debug=True عند التشغيل داخل Docker.
- استخدم متغيرات البيئة للأسرار.
- استخدم HTTPS وقاعدة بيانات إنتاجية عند النشر الحقيقي.

---

## 15. الخاتمة

يوفر Docker طريقة سهلة وثابتة لتشغيل النظام المصرفي الآمن على أجهزة مختلفة.
يمكن بناء وتشغيل المشروع باستخدام الأمر:

docker compose -f docker/docker-compose.yml up --build
ثم فتح التطبيق عبر:

http://localhost:5000