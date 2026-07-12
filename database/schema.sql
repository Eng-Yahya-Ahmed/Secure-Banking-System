-- =========================================================
-- Secure Banking System
-- Database Schema
-- SQLite
-- =========================================================

-- تفعيل التحقق من المفاتيح الأجنبية في SQLite
PRAGMA foreign_keys = ON;


-- =========================================================
-- جدول المستخدمين
-- =========================================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username VARCHAR(30) NOT NULL UNIQUE,

    email VARCHAR(120) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL DEFAULT 'customer'
        CHECK (role IN ('customer', 'admin')),

    is_active BOOLEAN NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- جدول الحسابات البنكية
-- =========================================================

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_number VARCHAR(12) NOT NULL UNIQUE,

    balance NUMERIC(15, 2) NOT NULL DEFAULT 1000.00
        CHECK (balance >= 0),

    user_id INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CHECK (
        LENGTH(account_number) = 12
        AND account_number NOT GLOB '*[^0-9A-F]*'
    )
);


-- =========================================================
-- جدول العمليات المالية
-- =========================================================

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sender_account_id INTEGER NOT NULL,

    receiver_account_id INTEGER NOT NULL,

    amount NUMERIC(15, 2) NOT NULL
        CHECK (amount > 0),

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sender_account_id)
        REFERENCES accounts(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (receiver_account_id)
        REFERENCES accounts(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CHECK (sender_account_id <> receiver_account_id)
);


-- =========================================================
-- الفهارس
-- =========================================================

-- تسريع البحث باستخدام اسم المستخدم
CREATE INDEX IF NOT EXISTS idx_users_username
ON users(username);


-- تسريع البحث باستخدام البريد الإلكتروني
CREATE INDEX IF NOT EXISTS idx_users_email
ON users(email);


-- تسريع البحث باستخدام رقم الحساب البنكي
CREATE INDEX IF NOT EXISTS idx_accounts_account_number
ON accounts(account_number);


-- تسريع البحث عن العمليات المرسلة
CREATE INDEX IF NOT EXISTS idx_transactions_sender
ON transactions(sender_account_id);


-- تسريع البحث عن العمليات المستلمة
CREATE INDEX IF NOT EXISTS idx_transactions_receiver
ON transactions(receiver_account_id);


-- تسريع ترتيب العمليات حسب التاريخ
CREATE INDEX IF NOT EXISTS idx_transactions_created_at
ON transactions(created_at);


-- =========================================================
-- منع الرصيد السالب
-- =========================================================

CREATE TRIGGER IF NOT EXISTS prevent_negative_balance_insert
BEFORE INSERT ON accounts
FOR EACH ROW
WHEN NEW.balance < 0
BEGIN
    SELECT RAISE(
        ABORT,
        'Account balance cannot be negative.'
    );
END;


CREATE TRIGGER IF NOT EXISTS prevent_negative_balance_update
BEFORE UPDATE OF balance ON accounts
FOR EACH ROW
WHEN NEW.balance < 0
BEGIN
    SELECT RAISE(
        ABORT,
        'Account balance cannot be negative.'
    );
END;


-- =========================================================
-- بيانات تجريبية اختيارية
-- =========================================================

-- لا تحفظ كلمات مرور حقيقية داخل هذا الملف.
-- القيم التالية أمثلة فقط، ولذلك بقيت معطلة بالتعليقات.
-- INSERT INTO users (
--     username,
--     email,
--     password_hash,
--     role,
--     is_active
-- )
-- VALUES (
--     'admin',
--     'admin@example.com',
--     'PLACE_A_BCRYPT_HASH_HERE',
--     'admin',
--     1
-- );


-- INSERT INTO accounts (
--     account_number,
--     balance,
--     user_id
-- )
-- VALUES (
--     'ABCDEF123456',
--     1000.00,
--     1
-- );


-- =========================================================
-- استعلامات مساعدة
-- =========================================================

-- عرض المستخدمين
-- SELECT * FROM users;


-- عرض الحسابات مع أسماء أصحابها
-- SELECT
--     accounts.id,
--     accounts.account_number,
--     accounts.balance,
--     users.username,
--     users.email
-- FROM accounts
-- JOIN users
--     ON accounts.user_id = users.id;


-- عرض العمليات مع أرقام الحسابات
-- SELECT
--     transactions.id,
--     sender.account_number AS sender_account,
--     receiver.account_number AS receiver_account,
--     transactions.amount,
--     transactions.created_at
-- FROM transactions
-- JOIN accounts AS sender
--     ON transactions.sender_account_id = sender.id
-- JOIN accounts AS receiver
--     ON transactions.receiver_account_id = receiver.id
-- ORDER BY transactions.created_at DESC;


-- حساب إجمالي الأموال داخل النظام
-- SELECT
--     ROUND(SUM(balance), 2) AS total_bank_balance
-- FROM accounts;


-- حساب عدد المستخدمين
-- SELECT COUNT(*) AS total_users
-- FROM users;


-- حساب عدد الحسابات البنكية
-- SELECT COUNT(*) AS total_accounts
-- FROM accounts;


-- حساب عدد العمليات المالية
-- SELECT COUNT(*) AS total_transactions
-- FROM transactions;


-- =========================================================
-- نهاية مخطط قاعدة البيانات
-- =========================================================