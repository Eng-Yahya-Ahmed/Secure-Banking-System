# مخططات النظام المصرفي الآمن

## 1. مقدمة

يحتوي هذا الملف على المخططات التي توضح معمارية النظام، وتدفق الطلبات، وآلية تسجيل الدخول، وتنفيذ التحويل المالي، والعلاقات بين مكونات المشروع.

تم إنشاء المخططات باستخدام لغة:

Mermaid
ويمكن عرضها من خلال إضافة:

Markdown Preview Enhanced
---

## 2. المخطط العام للنظام

يوضح المخطط التالي المكونات الأساسية للنظام المصرفي الآمن:

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
---

## 3. طبقات النظام

يعتمد النظام على عدة طبقات منفصلة:

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
---

## 5. مخطط تسجيل مستخدم جديد

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
---

## 6. مخطط تسجيل الدخول

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
---

## 7. مخطط تنفيذ التحويل المالي

`mermaid
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

---

## 8. التسلسل التفصيلي للتحويل المالي

mermaid
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

---

## 9. مخطط قاعدة البيانات

mermaid
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

---

## 10. مخطط المصادقة والصلاحيات

mermaid
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

---

## 11. صلاحيات المستخدمين

mermaid
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

---

## 12. مخطط تشفير كلمة المرور

mermaid
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

---

## 13. مخطط حماية النماذج باستخدام CSRF

mermaid
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

---

## 14. مخطط تحديد عدد المحاولات

mermaid
flowchart TD

    A[استقبال الطلب] --> B[Flask-Limiter]

    B --> C{هل تجاوز المستخدم الحد؟}

    C -- لا --> D[تنفيذ الطلب]

    C -- نعم --> E[رفض الطلب]

    E --> F[عرض صفحة 429]

    F --> G[الانتظار حتى انتهاء مدة التقييد]

---

## 15. مخطط معالجة الأخطاء

mermaid
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

---

## 16. مخطط الاختبارات الآلية

mermaid
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

---

## 17. دورة حياة المستخدم

mermaid
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

---

## 18. مخطط ملفات المشروع

mermaid
flowchart TD

    A[secure_Banking_System_pro]

    A --> B[backend]

    A --> C[tests]

    A --> D[docs]

    A --> E[database]

    A --> F[docker]

    A --> G[frontend]

    A --> H[.github]

    B --> I[app]

    B --> J[instance]

    B --> K[config.py]

    B --> L[requirements.txt]

    B --> M[run.py]

    I --> N[models]

    I --> O[routes]

    I --> P[security]

    I --> Q[services]

    I --> R[templates]

    I --> S[static]

    C --> T[test_pages.py]

    C --> U[test_auth.py]

    C --> V[test_transfer.py]

    D --> W[project_report.md]

    D --> X[database_design.md]

    D --> Y[security_features.md]

    D --> Z[testing_report.md]

    D --> AA[user_guide.md]

    D --> AB[diagrams]
`

---

## 19. الخاتمة

توضح هذه المخططات طريقة عمل النظام المصرفي الآمن من مرحلة استقبال طلب المستخدم حتى معالجة البيانات وحفظها في قاعدة البيانات.

كما توضح آلية التسجيل، تسجيل الدخول، تنفيذ التحويل، التحكم في الصلاحيات، تشفير كلمات المرور، حماية CSRF، معالجة الأخطاء، وتنفيذ الاختبارات الآلية.

تساعد هذه المخططات على فهم النظام بصورة أسرع، كما تسهل شرح المشروع أثناء العرض أو المناقشة.