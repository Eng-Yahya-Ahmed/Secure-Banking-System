from app.extensions import bcrypt


def hash_password(password: str) -> str:
    """تشفير كلمة المرور قبل حفظها."""

    password_hash = bcrypt.generate_password_hash(
        password
    )

    return password_hash.decode("utf-8")


def check_password(
    password_hash: str,
    password: str
) -> bool:
    """مقارنة كلمة المرور بالنسخة المشفرة."""

    if not password_hash or not password:
        return False

    try:
        return bcrypt.check_password_hash(
            password_hash,
            password
        )

    except (ValueError, TypeError):
        return False