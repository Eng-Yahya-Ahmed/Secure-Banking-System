import re
from decimal import Decimal, InvalidOperation


USERNAME_PATTERN = re.compile(
    r"^[A-Za-z0-9_]{3,30}$"
)

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

ACCOUNT_NUMBER_PATTERN = re.compile(
    r"^[A-F0-9]{12}$"
)


def validate_username(username: str) -> bool:
    """التحقق من اسم المستخدم."""

    if not isinstance(username, str):
        return False

    username = username.strip()

    return bool(
        USERNAME_PATTERN.fullmatch(username)
    )


def validate_email(email: str) -> bool:
    """التحقق من البريد الإلكتروني."""

    if not isinstance(email, str):
        return False

    email = email.strip().lower()

    return bool(
        EMAIL_PATTERN.fullmatch(email)
    )


def validate_password(password: str) -> bool:
    """
    التحقق من قوة كلمة المرور.

    الشروط:
    - 12 حرفًا على الأقل.
    - حرف كبير.
    - حرف صغير.
    - رقم.
    - رمز خاص.
    - بدون مسافات.
    """

    if not isinstance(password, str):
        return False

    if len(password) < 12:
        return False

    if any(character.isspace() for character in password):
        return False

    if re.search(r"[A-Z]", password) is None:
        return False

    if re.search(r"[a-z]", password) is None:
        return False

    if re.search(r"\d", password) is None:
        return False

    if re.search(r"[^\w\s]", password) is None:
        return False

    return True


def validate_account_number(
    account_number: str
) -> tuple[bool, str]:
    """
    التحقق من رقم الحساب.

    ترجع قيمتين:
    - حالة الرقم.
    - رسالة الخطأ.
    """

    if not isinstance(account_number, str):
        return False, "Enter a valid account number."

    account_number = account_number.strip().upper()

    if not account_number:
        return False, "Account number is required."

    if not ACCOUNT_NUMBER_PATTERN.fullmatch(account_number):
        return (
            False,
            "Enter a valid 12-character account number."
        )

    return True, ""


def validate_amount(
    amount_text: str
) -> tuple[bool, str, Decimal | None]:
    """
    التحقق من مبلغ التحويل.

    ترجع ثلاث قيم:
    - حالة المبلغ.
    - رسالة الخطأ.
    - المبلغ بعد التحويل إلى Decimal.
    """

    if not isinstance(amount_text, str):
        return False, "Enter a valid amount.", None

    amount_text = amount_text.strip()

    if not amount_text:
        return False, "Amount is required.", None

    try:
        amount = Decimal(amount_text)

    except (InvalidOperation, TypeError, ValueError):
        return False, "Enter a valid amount.", None

    if not amount.is_finite():
        return False, "Enter a valid amount.", None

    if amount <= Decimal("0.00"):
        return (
            False,
            "Amount must be greater than zero.",
            None
        )

    exponent = amount.as_tuple().exponent

    if not isinstance(exponent, int):
        return False, "Enter a valid amount.", None

    if exponent < -2:
        return (
            False,
            "Amount may contain no more than two decimal places.",
            None
        )

    if amount > Decimal("1000000.00"):
        return (
            False,
            "Amount exceeds the permitted transfer limit.",
            None
        )

    return True, "", amount