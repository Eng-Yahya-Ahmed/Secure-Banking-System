import sys
from pathlib import Path

import pytest


# تحديد مسار المشروع الرئيسي
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# تحديد مسار مجلد backend
BACKEND_PATH = PROJECT_ROOT / "backend"

# السماح للاختبارات باستيراد التطبيق من backend
sys.path.insert(
    0,
    str(BACKEND_PATH)
)


from app import create_app
from app.extensions import db


@pytest.fixture()
def app(tmp_path):
    """
    إنشاء نسخة تجريبية من التطبيق
    مع قاعدة بيانات مؤقتة ومنفصلة.
    """

    test_database = tmp_path / "test_banking.db"

    test_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "SQLALCHEMY_DATABASE_URI": (
                f"sqlite:///{test_database}"
            ),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,

            # تعطيل CSRF أثناء الاختبارات فقط
            "WTF_CSRF_ENABLED": False,

            # تعطيل Rate Limiting أثناء الاختبارات
            "RATELIMIT_ENABLED": False
        }
    )

    with test_app.app_context():

        # حذف أي جداول تجريبية قديمة
        db.drop_all()

        # إنشاء جداول جديدة للاختبار
        db.create_all()

        yield test_app

        # تنظيف قاعدة البيانات بعد الاختبار
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """
    متصفح تجريبي لإرسال الطلبات إلى التطبيق.
    """

    return app.test_client()


@pytest.fixture()
def runner(app):
    """
    أداة لتشغيل أوامر Flask أثناء الاختبار.
    """

    return app.test_cli_runner()