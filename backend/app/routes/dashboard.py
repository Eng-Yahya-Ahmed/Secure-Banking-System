from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from app.models.user import User
from app.models.account import Account
from app.models.transactions import Transaction
from app.security.hashing import check_password
from app.security.validation import (
    validate_username,
    validate_email
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    """
    عرض لوحة المستخدم وحسابه وآخر خمس عمليات مالية.
    """

    account = Account.query.filter_by(
        user_id=current_user.id
    ).first()

    latest_transactions = []

    if account is not None:

        latest_transactions = Transaction.query.filter(
            (
                Transaction.sender_account_id == account.id
            )
            |
            (
                Transaction.receiver_account_id == account.id
            )
        ).order_by(
            Transaction.created_at.desc()
        ).limit(5).all()

    return render_template(
        "dashboard.html",
        account=account,
        latest_transactions=latest_transactions
    )


@dashboard_bp.route("/profile")
@login_required
def profile():
    """
    عرض بيانات المستخدم والحساب البنكي.
    """

    account = Account.query.filter_by(
        user_id=current_user.id
    ).first()

    return render_template(
        "profile.html",
        account=account
    )


@dashboard_bp.route(
    "/profile/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():
    """
    تعديل اسم المستخدم والبريد الإلكتروني
    بعد التحقق من كلمة المرور الحالية.
    """

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        current_password = request.form.get(
            "current_password",
            ""
        )

        # التأكد من إدخال جميع الحقول
        if (
            not username
            or not email
            or not current_password
        ):
            flash(
                "All fields are required.",
                "danger"
            )

            return render_template(
                "edit_profile.html"
            )

        # التحقق من صحة اسم المستخدم
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
                "edit_profile.html"
            )

        # التحقق من صحة البريد الإلكتروني
        if not validate_email(email):

            flash(
                "Please enter a valid email address.",
                "danger"
            )

            return render_template(
                "edit_profile.html"
            )

        # التحقق من كلمة المرور الحالية
        if not check_password(
            current_user.password_hash,
            current_password
        ):
            flash(
                "Current password is incorrect.",
                "danger"
            )

            return render_template(
                "edit_profile.html"
            )

        # منع استخدام اسم مستخدم موجود لمستخدم آخر
        username_owner = User.query.filter(
            User.username == username,
            User.id != current_user.id
        ).first()

        if username_owner is not None:

            flash(
                "Username is already in use.",
                "danger"
            )

            return render_template(
                "edit_profile.html"
            )
        # منع استخدام بريد إلكتروني موجود لمستخدم آخر
        email_owner = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if email_owner is not None:

            flash(
                "Email address is already in use.",
                "danger"
            )

            return render_template(
                "edit_profile.html"
            )

        try:

            current_user.username = username
            current_user.email = email

            db.session.commit()

            flash(
                "Profile updated successfully.",
                "success"
            )

            return redirect(
                url_for("dashboard.profile")
            )

        except Exception:

            db.session.rollback()

            flash(
                (
                    "Profile could not be updated. "
                    "Please try again."
                ),
                "danger"
            )

    return render_template(
        "edit_profile.html"
    )