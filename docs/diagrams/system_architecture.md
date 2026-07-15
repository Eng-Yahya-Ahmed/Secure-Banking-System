# مخططات النظام المصرفي الآمن

## 1. مقدمة

يحتوي هذا الملف على المخططات التي توضح معمارية النظام، وتدفق الطلبات، وآلية تسجيل الدخول، وتنفيذ التحويل المالي، والعلاقات بين مكونات المشروع.

تم إنشاء المخططات باستخدام لغة:

يمكن عرض مخططات Mermaid مباشرة على GitHub عند وضعها داخل كتل `mermaid`،
كما يمكن معاينتها داخل VS Code باستخدام إضافة تدعم Mermaid.

Markdown Preview Enhanced
---

## 2. المخطط العام للنظام

يوضح المخطط التالي المكونات الأساسية للنظام المصرفي الآمن:

```mermaid
flowchart TD

    A[المستخدم] --> B[متصفح الويب]

    B --> C[تطبيق Flask]

    C --> D[Routes]
    C --> E[Security]
    C --> F[Models]
    C --> G[Templates]

    D --> H[Authentication Routes]
    D --> I[Dashboard Routes]
    D --> J[Transfer Routes]
    D --> K[Admin Routes]

    E --> L[Password Hashing]
    E --> M[Input Validation]
    E --> N[CSRF Protection]
    E --> O[Rate Limiting]

    F --> P[User Model]
    F --> Q[Account Model]
    F --> R[Transaction Model]

    P --> S[(SQLite Database)]
    Q --> S
    R --> S

    G --> T[HTML Pages]
    T --> B
```

---

## 3. طبقات النظام

يعتمد النظام على عدة طبقات منفصلة:

```mermaid
flowchart TB

    A[Presentation Layer]

    B[Route Layer]

    C[Security and Validation Layer]

    D[Business Logic Layer]

    E[Data Access Layer]

    F[(Database)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

### طبقة العرض

تتكون من:

- صفحات HTML.
- ملفات CSS.
- Bootstrap.
- قوالب Jinja2.

### طبقة المسارات

تستقبل طلبات المستخدم وتوجهها إلى الوظائف المناسبة.

### طبقة الأمان والتحقق

تتحقق من:

- تسجيل الدخول.
- صلاحية المستخدم.
- صحة المدخلات.
- قوة كلمة المرور.
- رقم الحساب.
- مبلغ التحويل.

### طبقة منطق النظام

تنفذ:

- إنشاء المستخدم.
- إنشاء الحساب.
- تسجيل الدخول.
- تنفيذ التحويل.
- إدارة المستخدمين.

### طبقة البيانات

تتولى التعامل مع قاعدة البيانات من خلال SQLAlchemy.

---

## 4. تدفق الطلب داخل النظام

يوضح المخطط كيف ينتقل طلب المستخدم داخل التطبيق:

```mermaid
sequenceDiagram

    actor User as المستخدم

    participant Browser as المتصفح

    participant Flask as تطبيق Flask

    participant Security as طبقة الأمان

    participant Database as قاعدة البيانات

    User->>Browser: إدخال البيانات

    Browser->>Flask: إرسال HTTP Request

    Flask->>Security: التحقق من الطلب

    Security-->>Flask: نتيجة التحقق

    alt البيانات صحيحة

        Flask->>Database: قراءة أو تعديل البيانات

        Database-->>Flask: إعادة النتيجة

        Flask-->>Browser: عرض الصفحة أو رسالة النجاح

        Browser-->>User: إظهار النتيجة

    else البيانات غير صحيحة

        Flask-->>Browser: رسالة خطأ

        Browser-->>User: إظهار سبب الرفض

    end
```

---

## 5. مخطط تسجيل مستخدم جديد

```mermaid
flowchart TD

    A[فتح صفحة التسجيل] --> B[إدخال البيانات]

    B --> C{هل الحقول مكتملة؟}

    C -- لا --> D[عرض رسالة خطأ]

    C -- نعم --> E{هل اسم المستخدم صالح؟}

    E -- لا --> D

    E -- نعم --> F{هل البريد صالح؟}

    F -- لا --> D

    F -- نعم --> G{هل كلمة المرور قوية؟}

    G -- لا --> D

    G -- نعم --> H{هل كلمتا المرور متطابقتان؟}

    H -- لا --> D

    H -- نعم --> I{هل اسم المستخدم موجود؟}

    I -- نعم --> D

    I -- لا --> J{هل البريد موجود؟}

    J -- نعم --> D

    J -- لا --> K[تشفير كلمة المرور]

    K --> L[إنشاء المستخدم]

    L --> M[إنشاء رقم حساب عشوائي]

    M --> N[إنشاء الحساب البنكي]

    N --> O[حفظ البيانات]

    O --> P[الانتقال إلى تسجيل الدخول]
```

---

## 6. مخطط تسجيل الدخول

```mermaid
flowchart TD

    A[فتح صفحة تسجيل الدخول] --> B[إدخال اسم المستخدم وكلمة المرور]

    B --> C{هل المستخدم موجود؟}

    C -- لا --> D[عرض رسالة دخول غير صحيحة]

    C -- نعم --> E{هل كلمة المرور صحيحة؟}

    E -- لا --> D

    E -- نعم --> F{هل الحساب فعال؟}

    F -- لا --> G[عرض رسالة الحساب معطل]

    F -- نعم --> H[إنشاء جلسة للمستخدم]

    H --> I{ما صلاحية المستخدم؟}

    I -- Admin --> J[الانتقال إلى لوحة المدير]

    I -- Customer --> K[الانتقال إلى لوحة المستخدم]
```

---

## 7. مخطط تنفيذ التحويل المالي

```mermaid
flowchart TD

    A[فتح صفحة التحويل] --> B[إدخال رقم المستلم والمبلغ]

    B --> C{هل رقم الحساب صالح؟}

    C -- لا --> D[رفض العملية]

    C -- نعم --> E{هل حساب المستلم موجود؟}

    E -- لا --> D
    E -- نعم --> F{هل حساب المستلم مختلف؟}

    F -- لا --> D

    F -- نعم --> G{هل المبلغ صالح؟}

    G -- لا --> D

    G -- نعم --> H{هل الرصيد كاف؟}

    H -- لا --> D

    H -- نعم --> I[خصم المبلغ من المرسل]

    I --> J[إضافة المبلغ إلى المستلم]

    J --> K[إنشاء سجل العملية]

    K --> L{هل تم الحفظ بنجاح؟}

    L -- نعم --> M[Commit]

    M --> N[عرض رسالة نجاح]

    L -- لا --> O[Rollback]

    O --> P[عرض رسالة خطأ]

```

---

## 8. التسلسل التفصيلي للتحويل المالي

```mermaid
sequenceDiagram

    actor Sender as المرسل

    participant Browser as المتصفح

    participant TransferRoute as Transfer Route

    participant Validation as Validation

    participant AccountModel as Account Model

    participant TransactionModel as Transaction Model

    participant Database as قاعدة البيانات

    Sender->>Browser: إدخال رقم الحساب والمبلغ

    Browser->>TransferRoute: POST /transfer

    TransferRoute->>Validation: فحص رقم الحساب

    Validation-->>TransferRoute: نتيجة الفحص

    TransferRoute->>Validation: فحص المبلغ

    Validation-->>TransferRoute: المبلغ بعد التحويل إلى Decimal

    TransferRoute->>AccountModel: البحث عن حساب المستلم

    AccountModel->>Database: SELECT Account

    Database-->>AccountModel: بيانات الحساب

    AccountModel-->>TransferRoute: حساب المستلم

    TransferRoute->>TransferRoute: مقارنة الحسابين

    TransferRoute->>TransferRoute: فحص الرصيد

    TransferRoute->>AccountModel: خصم وإضافة المبلغ

    TransferRoute->>TransactionModel: إنشاء سجل التحويل

    TransferRoute->>Database: COMMIT

    Database-->>TransferRoute: تم الحفظ

    TransferRoute-->>Browser: رسالة نجاح

    Browser-->>Sender: عرض الرصيد الجديد

```

---

## 9. مخطط قاعدة البيانات

```mermaid
erDiagram

    USERS -- ACCOUNTS : owns

    ACCOUNTS ||--o{ TRANSACTIONS : sends

    ACCOUNTS ||--o{ TRANSACTIONS : receives

    USERS {
        integer id PK
        string username UK
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime created_at
    }

    ACCOUNTS {
        integer id PK
        string account_number UK
        decimal balance
        integer user_id FK
    }

    TRANSACTIONS {
        integer id PK
        integer sender_account_id FK
        integer receiver_account_id FK
        decimal amount
        datetime created_at
    }

```

---

## 10. مخطط المصادقة والصلاحيات

```mermaid
flowchart TD

    A[طلب فتح صفحة] --> B{هل الصفحة عامة؟}

    B -- نعم --> C[السماح بالوصول]

    B -- لا --> D{هل المستخدم مسجل؟}

    D -- لا --> E[التحويل إلى صفحة Login]

    D -- نعم --> F{هل الصفحة خاصة بالمدير؟}

    F -- لا --> C

    F -- نعم --> G{هل دور المستخدم Admin؟}

    G -- نعم --> C

    G -- لا --> H[عرض خطأ 403]

```

---

## 11. صلاحيات المستخدمين

```mermaid
flowchart LR

    A[Customer]

    B[Admin]

    A --> C[Dashboard]
    A --> D[Transfer]
    A --> E[Transactions]
    A --> F[Profile]
    A --> G[Change Password]

    B --> H[Admin Dashboard]
    B --> I[View Users]
    B --> J[View Accounts]
    B --> K[View Transactions]
    B --> L[Disable User]
    B --> M[Enable User]
    B --> N[Delete User]

```

---

## 12. مخطط تشفير كلمة المرور

```mermaid
flowchart TD

    A[كلمة المرور الأصلية] --> B[Flask-Bcrypt]

    B --> C[إنشاء Salt]

    C --> D[إنشاء Password Hash]

    D --> E[(حفظ القيمة المشفرة)]

    F[تسجيل الدخول] --> G[إدخال كلمة المرور]

    G --> H[مقارنة كلمة المرور مع Hash]

    E --> H

    H --> I{هل متطابقة؟}

    I -- نعم --> J[السماح بتسجيل الدخول]

    I -- لا --> K[رفض تسجيل الدخول]

```

---

## 13. مخطط حماية النماذج باستخدام CSRF

```mermaid
sequenceDiagram

    actor User as المستخدم

    participant Browser as المتصفح

    participant Flask as Flask Server

    participant CSRF as CSRF Protection

    User->>Browser: فتح النموذج

    Browser->>Flask: GET Request

    Flask->>CSRF: إنشاء CSRF Token

    CSRF-->>Flask: Token

    Flask-->>Browser: النموذج مع Token

    User->>Browser: إرسال النموذج

    Browser->>Flask: POST Request مع Token

    Flask->>CSRF: التحقق من Token

    alt Token صحيح
    CSRF-->>Flask: السماح بالطلب

        Flask-->>Browser: تنفيذ العملية

    else Token غير صحيح

        CSRF-->>Flask: رفض الطلب

        Flask-->>Browser: خطأ أمني

    end

```

---

## 14. مخطط تحديد عدد المحاولات

```mermaid
flowchart TD

    A[استقبال الطلب] --> B[Flask-Limiter]

    B --> C{هل تجاوز المستخدم الحد؟}

    C -- لا --> D[تنفيذ الطلب]

    C -- نعم --> E[رفض الطلب]

    E --> F[عرض صفحة 429]

    F --> G[الانتظار حتى انتهاء مدة التقييد]

```

---

## 15. مخطط معالجة الأخطاء

```mermaid
flowchart TD

    A[تنفيذ الطلب] --> B{هل حدث خطأ؟}

    B -- لا --> C[إكمال العملية]

    B -- نعم --> D{نوع الخطأ}

    D --> E[403 Access Denied]

    D --> F[404 Page Not Found]

    D --> G[429 Too Many Requests]

    D --> H[500 Internal Server Error]

    H --> I[Database Rollback]

    E --> J[عرض صفحة الخطأ]

    F --> J

    G --> J

    I --> J

```

---

## 16. مخطط الاختبارات الآلية

```mermaid
flowchart TD

    A[تشغيل Pytest] --> B[إنشاء تطبيق اختبار]

    B --> C[إنشاء قاعدة بيانات مؤقتة]

    C --> D[تشغيل اختبارات الصفحات]

    C --> E[تشغيل اختبارات المصادقة]

    C --> F[تشغيل اختبارات التحويل]

    D --> G[جمع النتائج]

    E --> G

    F --> G

    G --> H{هل توجد اختبارات فاشلة؟}

    H -- لا --> I[25 Passed]

    H -- نعم --> J[عرض تفاصيل الخطأ]

    I --> K[حذف قاعدة بيانات الاختبار]

    J --> K

```

---

## 17. دورة حياة المستخدم

```mermaid
stateDiagram-v2

    [*] --> Registered

    Registered --> Active

    Active --> LoggedIn

    LoggedIn --> Dashboard

    Dashboard --> Transfer

    Dashboard --> Transactions

    Dashboard --> Profile

    Transfer --> Dashboard

    Transactions --> Dashboard

    Profile --> Dashboard

    Dashboard --> LoggedOut

    Active --> Disabled

    Disabled --> Active

    LoggedOut --> LoggedIn

    LoggedOut --> [*]

```

---

## 18. مخطط ملفات المشروع

```mermaid
flowchart TD
    ROOT[secure_Banking_System_pro]

    ROOT --> BACKEND[backend]
    ROOT --> TESTS[tests]
    ROOT --> DOCS[docs]
    ROOT --> DATABASE[database]
    ROOT --> DOCKER[docker]
    ROOT --> FRONTEND[frontend]
    ROOT --> GITHUB[.github]

    BACKEND --> APP[app]
    BACKEND --> INSTANCE[instance]
    BACKEND --> CONFIG[config.py]
    BACKEND --> REQ[requirements.txt]
    BACKEND --> RUN[run.py]

    APP --> MODELS[models]
    APP --> ROUTES[routes]
    APP --> SECURITY[security]
    APP --> TEMPLATES[templates]
    APP --> STATIC[static]
    APP --> EXT[extensions.py]

    SECURITY --> HEADERS[headers.py]
    SECURITY --> HASHING[hashing.py]
    SECURITY --> VALIDATION[validation.py]
    SECURITY --> CSRF_FILE[csrf.py]

    TESTS --> TEST_PAGES[test_pages.py]
    TESTS --> TEST_AUTH[test_auth.py]
    TESTS --> TEST_TRANSFER[test_transfer.py]
    TESTS --> CONFTEST[conftest.py]

    DOCS --> PROJECT_REPORT[project_report.md]
    DOCS --> DB_DESIGN[database_design.md]
    DOCS --> SECURITY_FEATURES[security_features.md]
    DOCS --> TESTING_REPORT[testing_report.md]
    DOCS --> USER_GUIDE[user_guide.md]
    DOCS --> SSDLC[ssdlc_report.md]
    DOCS --> THREAT[threat_model.md]
    DOCS --> DIAGRAMS[diagrams]
    DOCS --> SECURITY_REPORTS[security_reports]

    GITHUB --> WORKFLOWS[workflows]
    WORKFLOWS --> TESTS_YML[tests.yml]
```

---

## 19. ملخص المخططات الوظيفية

توضح هذه المخططات طريقة عمل النظام المصرفي الآمن من مرحلة استقبال طلب المستخدم حتى معالجة البيانات وحفظها في قاعدة البيانات.

كما توضح آلية التسجيل، تسجيل الدخول، تنفيذ التحويل، التحكم في الصلاحيات، تشفير كلمات المرور، حماية CSRF، معالجة الأخطاء، وتنفيذ الاختبارات الآلية.

تساعد هذه المخططات على فهم النظام بصورة أسرع، كما تسهل شرح المشروع أثناء العرض أو المناقشة.

---

## 20. مخطط المعمارية الأمنية

يوضح المخطط التالي أماكن تطبيق الضوابط الأمنية بين المستخدم والتطبيق وقاعدة البيانات:

```mermaid
flowchart TD
    USER[المستخدم] --> BROWSER[متصفح الويب]
    BROWSER -->|HTTP Requests| PORT[Docker Port 127.0.0.1:5000]
    PORT --> FLASK[Flask Application]

    FLASK --> RATE[Rate Limiting]
    FLASK --> CSRF[CSRF Protection]
    FLASK --> AUTH[Authentication]
    FLASK --> RBAC[Role-Based Access Control]
    FLASK --> VALIDATION[Input Validation]
    FLASK --> HEADERS[Security Headers]

    VALIDATION --> LOGIC[Business Logic]
    AUTH --> LOGIC
    RBAC --> LOGIC

    LOGIC --> ORM[SQLAlchemy ORM]
    ORM --> DB[(SQLite Database)]

    BROWSER -->|Bootstrap Resources| CDN[jsDelivr CDN]
    CDN --> SRI[Subresource Integrity]
```

---

## 21. طبقات الحماية الأمنية

يستخدم المشروع مبدأ الدفاع متعدد الطبقات، بحيث لا يعتمد الأمان على إجراء واحد فقط:

```mermaid
flowchart LR
    REQUEST[HTTP Request] --> LIMITER[Rate Limiting]
    LIMITER --> CSRF_CHECK[CSRF Validation]
    CSRF_CHECK --> LOGIN_CHECK[Authentication]
    LOGIN_CHECK --> ROLE_CHECK[Authorization]
    ROLE_CHECK --> INPUT_CHECK[Input Validation]
    INPUT_CHECK --> BUSINESS[Business Logic]
    BUSINESS --> ORM_LAYER[SQLAlchemy ORM]
    ORM_LAYER --> DATABASE_LAYER[(Database)]

    BUSINESS --> RESPONSE[HTTP Response]
    RESPONSE --> SECURITY_HEADERS[Security Headers]
    SECURITY_HEADERS --> CLIENT[User Browser]
```

### الضوابط المطبقة

- تشفير كلمات المرور باستخدام Bcrypt.
- حماية الجلسات باستخدام Flask-Login.
- حماية النماذج باستخدام CSRF Token.
- تحديد عدد الطلبات باستخدام Flask-Limiter.
- التحقق من المدخلات داخل الخادم.
- التحكم في الوصول بناءً على دور المستخدم.
- استخدام SQLAlchemy ORM.
- إضافة Content Security Policy.
- إضافة X-Frame-Options وX-Content-Type-Options.
- إضافة Referrer-Policy وPermissions-Policy.
- حماية Cookies باستخدام HttpOnly وSameSite.
- التحقق من ملفات Bootstrap الخارجية باستخدام Subresource Integrity.
- استخدام Commit وRollback للمحافظة على اتساق التحويلات.

---

## 22. حدود الثقة

تمثل حدود الثقة النقاط التي تنتقل عندها البيانات بين مناطق ذات مستويات ثقة مختلفة:

```mermaid
flowchart LR
    subgraph UNTRUSTED[منطقة غير موثوقة]
        USER_EXT[المستخدم]
        BROWSER_EXT[المتصفح]
    end

    subgraph APP_ZONE[منطقة التطبيق]
        CONTAINER[Docker Container]
        FLASK_APP[Flask Application]
        CONTROLS[Security Controls]
    end

    subgraph DATA_ZONE[منطقة البيانات]
        SQLITE[(SQLite Database)]
    end

    USER_EXT --> BROWSER_EXT
    BROWSER_EXT -->|Untrusted Input| CONTAINER
    CONTAINER --> FLASK_APP
    FLASK_APP --> CONTROLS
    CONTROLS --> SQLITE
```

### الحدود الرئيسية

1. **المستخدم والمتصفح:** جميع البيانات القادمة من المستخدم تعد غير موثوقة.
2. **المتصفح وتطبيق Flask:** يجب التحقق من الطلب والمصادقة والصلاحيات وCSRF.
3. **التطبيق وقاعدة البيانات:** لا يتم الوصول إلى البيانات إلا من خلال SQLAlchemy.
4. **التطبيق والموارد الخارجية:** يتم التحقق من ملفات CDN باستخدام SRI.
5. **الجهاز المضيف وحاوية Docker:** التطبيق معزول داخل الحاوية ومتاح محليًا فقط.

---

## 23. مخطط الاختبارات الأمنية

```mermaid
flowchart TD
    SOURCE[Python Source Code] --> BANDIT[Bandit SAST]
    RUNNING_APP[Running Flask Application] --> ZAP[OWASP ZAP DAST]
    TEST_CODE[Automated Test Suite] --> PYTEST[Pytest]
    REPOSITORY[GitHub Repository] --> ACTIONS[GitHub Actions]

    BANDIT --> SECURITY_REPORTS[Security Reports]
    ZAP --> SECURITY_REPORTS
    PYTEST --> TEST_RESULTS[Test Results]
    ACTIONS --> TEST_RESULTS
```

### النتائج النهائية

| الاختبار | الأداة | النتيجة |
|---|---|---|
| الاختبارات البرمجية | Pytest | 25 اختبارًا ناجحًا |
| SAST | Bandit | لا توجد مشكلات أمنية مصنفة |
| DAST | OWASP ZAP | 0 High، 0 Medium، 0 Low |
| التكامل المستمر | GitHub Actions | ناجح |

تم تنفيذ فحص OWASP ZAP كفحص Baseline أولي غير مصادق عليه للصفحات العامة.

---

## 24. بنية التشغيل الحالية باستخدام Docker

```mermaid
flowchart TD
    LOCAL_USER[المستخدم المحلي] --> LOCAL_BROWSER[المتصفح]
    LOCAL_BROWSER -->|http://localhost:5000| HOST_PORT[127.0.0.1:5000]
    HOST_PORT --> CONTAINER_APP[Docker Container]
    CONTAINER_APP --> FLASK_SERVER[Flask Application]
    FLASK_SERVER --> SQLALCHEMY[SQLAlchemy]
    SQLALCHEMY --> LOCAL_DB[(SQLite Database)]
```

### خصائص التشغيل الحالي

- التطبيق يعمل داخل Docker.
- المنفذ مرتبط بالجهاز المحلي فقط.
- قاعدة البيانات محفوظة خارج طبقات الحاوية المؤقتة.
- المشروع مخصص للعرض الأكاديمي والتطوير المحلي.
- لم يتم نشر التطبيق على خادم إنتاج عام.

---

## 25. البنية المقترحة لبيئة الإنتاج

```mermaid
flowchart TD
    PROD_USER[المستخدم] --> HTTPS[HTTPS]
    HTTPS --> NGINX[Nginx Reverse Proxy]
    NGINX --> GUNICORN[Gunicorn WSGI Server]
    GUNICORN --> PROD_FLASK[Flask Application]

    PROD_FLASK --> POSTGRES[(PostgreSQL)]
    PROD_FLASK --> AUDIT[Audit Logging]
    PROD_FLASK --> MFA[MFA and Email Service]
    PROD_FLASK --> SECRETS[Secret Management]

    MONITORING[Security Monitoring] --> PROD_FLASK
    BACKUPS[Automated Backups] --> POSTGRES
```

### التحسينات المقترحة للإنتاج

- استخدام HTTPS.
- استخدام Nginx وGunicorn.
- الانتقال من SQLite إلى PostgreSQL.
- إضافة المصادقة الثنائية.
- إضافة سجل تدقيق أمني شامل.
- استخدام نظام آمن لإدارة الأسرار.
- إضافة مراقبة وتنبيهات أمنية.
- إنشاء نسخ احتياطية تلقائية.
- تنفيذ فحص ZAP مصادق عليه للصفحات الداخلية.

---

## 26. القيود الحالية

- المشروع تطبيق Flask موحد وليس Microservices.
- لا يوجد API Gateway.
- التشغيل الحالي محلي عبر HTTP.
- لا توجد مصادقة ثنائية.
- لا يوجد تحقق من البريد الإلكتروني.
- لا يوجد Audit Logging شامل.
- قاعدة البيانات الحالية SQLite.
- يتم استخدام Flask Development Server.
- فحص OWASP ZAP الحالي غير مصادق عليه.
- لا توجد مراقبة مركزية أو نسخ احتياطية تلقائية.
- المشروع نموذج أكاديمي وليس نظامًا مصرفيًا إنتاجيًا حقيقيًا.

---

## 27. الخاتمة

توضح المخططات البنية الوظيفية والأمنية لنظام Secure Banking System، بدءًا من استقبال طلب المستخدم، مرورًا بالمصادقة والتحقق من المدخلات وتنفيذ منطق التحويل، وصولًا إلى حفظ البيانات داخل قاعدة البيانات.

كما توضح المخططات تطبيق مبدأ الدفاع متعدد الطبقات، وحدود الثقة، وتشغيل المشروع داخل Docker، وربط الاختبارات البرمجية والأمنية بدورة حياة تطوير البرمجيات الآمنة.

تم الحفاظ على المخططات الوظيفية الأصلية وإضافة المعمارية الأمنية، والاختبارات الأمنية، وبنية التشغيل الحالية، والبنية المقترحة للإنتاج، والقيود الحالية، مما يجعل المستند أكثر اكتمالًا وملاءمة للعرض والمناقشة.