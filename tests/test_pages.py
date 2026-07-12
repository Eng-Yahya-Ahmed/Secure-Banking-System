def test_login_page_opens(client):
    """
    التأكد من أن صفحة تسجيل الدخول تعمل.
    """

    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page_opens(client):
    """
    التأكد من أن صفحة التسجيل تعمل.
    """

    response = client.get("/register")

    assert response.status_code == 200
    assert b"Create Account" in response.data


def test_unknown_page_returns_404(client):
    """
    التأكد من أن الرابط غير الموجود يعيد خطأ 404.
    """

    response = client.get("/unknown-test-page")

    assert response.status_code == 404
    assert b"404" in response.data


def test_dashboard_requires_login(client):
    """
    منع الزائر من دخول لوحة المستخدم.
    """

    response = client.get(
        "/dashboard",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_transfer_requires_login(client):
    """
    منع الزائر من دخول صفحة التحويل.
    """

    response = client.get(
        "/transfer",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_transactions_requires_login(client):
    """
    منع الزائر من مشاهدة سجل العمليات.
    """

    response = client.get(
        "/transactions",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_requires_login(client):
    """
    منع الزائر من فتح الملف الشخصي.
    """

    response = client.get(
        "/profile",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_change_password_requires_login(client):
    """
    منع الزائر من فتح صفحة تغيير كلمة المرور.
    """

    response = client.get(
        "/change-password",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_admin_requires_login(client):
    """
    منع الزائر من دخول لوحة المدير.
    """

    response = client.get(
        "/admin",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]