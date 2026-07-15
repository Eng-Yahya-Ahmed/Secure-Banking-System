from flask import Flask, render_template

from config import Config

from app.extensions import (
    db,
    bcrypt,
    login_manager,
    csrf,
    limiter
)


def create_app(test_config=None):
    """
    إنشاء تطبيق Flask وتهيئة جميع الإضافات والمسارات.
    """

    app = Flask(__name__)

    # تحميل إعدادات المشروع من config.py
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    # تهيئة الإضافات
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # إعدادات Flask-Login
    login_manager.login_view = "auth.login" # type : ignore [assignment]
    login_manager.login_message = (
        "Please log in to access this page."
    )
    login_manager.login_message_category = "warning"

    # تحميل المستخدم من قاعدة البيانات
    @login_manager.user_loader
    def load_user(user_id):

        from app.models.user import User

        try:
            return db.session.get(
                User,
                int(user_id)
            )

        except (ValueError, TypeError):
            return None

    # استيراد الموديلات حتى يتعرف SQLAlchemy على الجداول
    from app.models.user import User
    from app.models.account import Account
    from app.models.transactions import Transaction

    # استيراد الـ Blueprints من مجلد routes
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transfer import transfer_bp
    from app.routes.transactions import transactions_bp
    from app.routes.admin import admin_bp
    from app.security.headers import register_security_headers

    # تسجيل الـ Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(admin_bp)
    

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template(
            "403.html"
        ), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "404.html"
        ), 404

    @app.errorhandler(429)
    def too_many_requests(error):
        return render_template(
            "429.html"
        ), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()

        return render_template(
            "500.html"
        ), 500

    with app.app_context():
        db.create_all()

    register_security_headers(app)
    return app