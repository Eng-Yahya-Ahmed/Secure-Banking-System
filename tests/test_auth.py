from app.extensions import db
from app.models.user import User
from app.models.account import Account


VALID_PASSWORD = "TestUser@12345"


def register_user(
    client,
    username="testuser",
    email="testuser@gmail.com",
    password=VALID_PASSWORD
):
    """
    دالة مساعدة لتسجيل مستخدم جديد أثناء الاختبارات.
    """

    return client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": password
        },
        follow_redirects=True
    )


def login_user(
    client,
    username="testuser",
    password=VALID_PASSWORD,
    follow_redirects=True
):
    """
    دالة مساعدة لتسجيل الدخول أثناء الاختبارات.
    """

    return client.post(
        "/login",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=follow_redirects
    )


def test_registration_creates_user_and_account(client, app):
    """
    التأكد من إنشاء المستخدم وحسابه البنكي تلقائيًا.
    """

    response = register_user(client)

    assert response.status_code == 200
    assert b"Registration completed successfully" in response.data

    with app.app_context():

        user = User.query.filter_by(
            username="testuser"
        ).first()

        assert user is not None
        assert user.email == "testuser@gmail.com"
        assert user.role == "customer"
        assert user.is_active is True

        account = Account.query.filter_by(
            user_id=user.id
        ).first()

        assert account is not None
        assert account.account_number is not None
        assert float(account.balance) == 1000.00


def test_duplicate_username_is_rejected(client):
    """
    منع تسجيل اسم مستخدم موجود مسبقًا.
    """

    register_user(client)

    response = register_user(
        client,
        username="testuser",
        email="another@gmail.com"
    )

    assert response.status_code == 200
    assert b"Username is already registered" in response.data


def test_duplicate_email_is_rejected(client):
    """
    منع تسجيل بريد إلكتروني موجود مسبقًا.
    """

    register_user(client)

    response = register_user(
        client,
        username="anotheruser",
        email="testuser@gmail.com"
    )

    assert response.status_code == 200
    assert b"Email address is already registered" in response.data


def test_weak_password_is_rejected(client, app):
    """
    التأكد من رفض كلمة المرور الضعيفة
    وعدم إنشاء المستخدم في قاعدة البيانات.
    """

    response = register_user(
        client,
        username="weakuser",
        email="weakuser@gmail.com",
        password="password"
    )

    assert response.status_code == 200

    with app.app_context():

        user = User.query.filter_by(
            username="weakuser"
        ).first()

        assert user is None


def test_password_confirmation_must_match(client):
    """
    التأكد من تطابق كلمتي المرور.
    """

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": VALID_PASSWORD,
            "confirm_password": "Different@12345"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Passwords do not match" in response.data


def test_user_can_login_with_correct_password(client):
    """
    تسجيل الدخول بالبيانات الصحيحة.
    """

    register_user(client)

    response = login_user(
        client,
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_wrong_password_is_rejected(client):
    """
    رفض تسجيل الدخول بكلمة مرور خاطئة.
    """

    register_user(client)

    response = login_user(
        client,
        password="WrongPassword@123",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_unknown_username_is_rejected(client):
    """
    رفض اسم مستخدم غير موجود.
    """
    response = login_user(
        client,
        username="unknownuser",
        password=VALID_PASSWORD,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_disabled_user_cannot_login(client, app):
    """
    منع المستخدم المعطّل من تسجيل الدخول.
    """

    register_user(client)

    with app.app_context():

        user = User.query.filter_by(
            username="testuser"
        ).first()
        assert user is not None
        user.is_active = False
        db.session.commit()

    response = login_user(
        client,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Your account has been disabled" in response.data 