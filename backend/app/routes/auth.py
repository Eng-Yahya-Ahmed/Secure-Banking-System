import secrets

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from app.extensions import db, limiter
from app.models.user import User
from app.models.account import Account

from app.security.hashing import (
    hash_password,
    check_password
)

from app.security.validation import (
    validate_username,
    validate_email,
    validate_password
)


auth_bp = Blueprint(
    "auth",
    __name__
)


def generate_account_number() -> str:
    """إنشاء رقم حساب بنكي فريد."""

    while True:

        account_number = secrets.token_hex(
            6
        ).upper()

        existing_account = Account.query.filter_by(
            account_number=account_number
        ).first()

        if existing_account is None:
            return account_number


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
@limiter.limit(
    "3 per hour",
    methods=["POST"],
    error_message=(
        "Too many registration attempts. "
        "Please try again later."
    )
)
def register():
    """إنشاء مستخدم وحساب بنكي جديد."""

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(
                url_for("admin.admin_dashboard")
            )

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if (
            not username
            or not email
            or not password
            or not confirm_password
        ):
            flash(
                "All fields are required.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        if not validate_username(username):
            flash(
                (
                    "Username must be between 3 and 30 "
                    "characters and contain only letters, "
                    "numbers and underscores."
                ),
                "danger"
            )

            return render_template(
                "register.html"
            )

        if not validate_email(email):
            flash(
                "Please enter a valid email address.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        if not validate_password(password):
            flash(
                (
                    "Password must be at least 12 characters "
                    "and contain uppercase, lowercase, "
                    "a number and a special character."
                ),
                "danger"
            )

            return render_template(
                "register.html"
            )

        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username is not None:
            flash(
                "Username is already registered.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email is not None:
            flash(
                "Email address is already registered.",
                "danger"
            )
            return render_template(
                "register.html"
            )

        try:
            # إنشاء المستخدم دون تمرير معاملات إلى constructor
            # لتجنب تحذيرات Pylance.
            new_user = User()

            new_user.username = username
            new_user.email = email
            new_user.password_hash = hash_password(
                password
            )
            new_user.role = "customer"
        

            db.session.add(new_user)
            db.session.flush()

            # إنشاء الحساب البنكي.
            new_account = Account()

            new_account.account_number = (
                generate_account_number()
            )
            new_account.user_id = new_user.id

            db.session.add(new_account)
            db.session.commit()

            flash(
                (
                    "Registration completed successfully. "
                    "You can now log in."
                ),
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        except Exception:
            db.session.rollback()

            flash(
                (
                    "Registration failed. "
                    "Please try again."
                ),
                "danger"
            )

    return render_template(
        "register.html"
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
@limiter.limit(
    "5 per minute",
    methods=["POST"],
    error_message=(
        "Too many login attempts. "
        "Please try again later."
    )
)
def login():
    """تسجيل دخول المستخدم."""

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(
                url_for("admin.admin_dashboard")
            )

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:
            flash(
                "Username and password are required.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        user = User.query.filter_by(
            username=username
        ).first()

        if user is None:
            flash(
                "Invalid username or password.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        if not check_password(
            user.password_hash,
            password
        ):
            flash(
                "Invalid username or password.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        if not user.is_active:
            flash(
                (
                    "Your account has been disabled. "
                    "Please contact the administrator."
                ),
                "danger"
            )

            return render_template(
                "login.html"
            )

        login_user(user)

        flash(
            "Login successful.",
            "success"
        )

        if user.role == "admin":
            return redirect(
                url_for("admin.admin_dashboard")
            )

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "login.html"
    )


@auth_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
@limiter.limit(
    "5 per hour",
    methods=["POST"],
    error_message=(
        "Too many password change attempts. "
        "Please try again later."
    )
)
def change_password():
    """تغيير كلمة مرور المستخدم."""

    if request.method == "POST":

        current_password = request.form.get(
            "current_password",
            ""
        )
        new_password = request.form.get(
            "new_password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if (
            not current_password
            or not new_password
            or not confirm_password
        ):
            flash(
                "All fields are required.",
                "danger"
            )

            return render_template(
                "change_password.html"
            )

        if not check_password(
            current_user.password_hash,
            current_password
        ):
            flash(
                "Current password is incorrect.",
                "danger"
            )

            return render_template(
                "change_password.html"
            )

        if new_password != confirm_password:
            flash(
                "New passwords do not match.",
                "danger"
            )

            return render_template(
                "change_password.html"
            )

        if not validate_password(new_password):
            flash(
                (
                    "Password must be at least 12 characters "
                    "and contain uppercase, lowercase, "
                    "a number and a special character."
                ),
                "danger"
            )

            return render_template(
                "change_password.html"
            )

        if check_password(
            current_user.password_hash,
            new_password
        ):
            flash(
                (
                    "The new password must be different "
                    "from the current password."
                ),
                "danger"
            )

            return render_template(
                "change_password.html"
            )

        try:
            current_user.password_hash = (
                hash_password(new_password)
            )

            db.session.commit()
            logout_user()

            flash(
                (
                    "Password changed successfully. "
                    "Please log in using your new password."
                ),
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        except Exception:
            db.session.rollback()

            flash(
                (
                    "The password could not be changed. "
                    "Please try again."
                ),
                "danger"
            )

    return render_template(
        "change_password.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():
    """تسجيل خروج المستخدم."""

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )