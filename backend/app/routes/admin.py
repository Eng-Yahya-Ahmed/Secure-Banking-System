from functools import wraps

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    abort
)

from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models.user import User
from app.models.account import Account
from app.models.transactions import Transaction


admin_bp = Blueprint("admin", __name__)


def admin_required(function):
    """
    يمنع المستخدم العادي من الوصول إلى صفحات المدير.
    """

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.role != "admin":
            abort(403)

        return function(*args, **kwargs)

    return decorated_function


@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    """
    عرض لوحة تحكم المدير.
    """

    users = User.query.order_by(User.id.asc()).all()

    accounts = Account.query.order_by(
        Account.id.asc()
    ).all()

    transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()

    users_count = User.query.count()
    accounts_count = Account.query.count()
    transactions_count = Transaction.query.count()

    total_balance = db.session.query(
        func.coalesce(func.sum(Account.balance), 0)
    ).scalar()

    return render_template(
        "admin.html",
        users=users,
        accounts=accounts,
        transactions=transactions,
        users_count=users_count,
        accounts_count=accounts_count,
        transactions_count=transactions_count,
        total_balance=total_balance
    )


@admin_bp.route(
    "/admin/users/<int:user_id>/disable",
    methods=["POST"]
)
@login_required
@admin_required
def disable_user(user_id):
    """
    تعطيل مستخدم ومنعه من تسجيل الدخول.
    """

    user = db.session.get(User, user_id)

    if user is None:
        abort(404)

    if user.id == current_user.id:
        flash(
            "You cannot disable your own account.",
            "danger"
        )

        return redirect(
            url_for("admin.admin_dashboard")
        )

    if user.role == "admin":
        flash(
            "Another administrator account cannot be disabled.",
            "danger"
        )

        return redirect(
            url_for("admin.admin_dashboard")
        )

    user.is_active = False

    try:
        db.session.commit()

        flash(
            "User disabled successfully.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "The user could not be disabled.",
            "danger"
        )

    return redirect(
        url_for("admin.admin_dashboard")
    )


@admin_bp.route(
    "/admin/users/<int:user_id>/enable",
    methods=["POST"]
)
@login_required
@admin_required
def enable_user(user_id):
    """
    إعادة تفعيل المستخدم.
    """

    user = db.session.get(User, user_id)

    if user is None:
        abort(404)

    user.is_active = True

    try:
        db.session.commit()

        flash(
            "User enabled successfully.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "The user could not be enabled.",
            "danger"
        )

    return redirect(
        url_for("admin.admin_dashboard")
    )


@admin_bp.route(
    "/admin/users/<int:user_id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete_user(user_id):
    """
    حذف المستخدم وحسابه وعملياته المالية.
    """

    user = db.session.get(User, user_id)

    if user is None:
        abort(404)

    if user.id == current_user.id:
        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(
            url_for("admin.admin_dashboard")
        )

    if user.role == "admin":
        flash(
            "Another administrator account cannot be deleted.",
            "danger"
        )
        return redirect(
            url_for("admin.admin_dashboard")
        )

    account = Account.query.filter_by(
        user_id=user.id
    ).first()

    try:
        if account is not None:

            Transaction.query.filter(
                (
                    Transaction.sender_account_id
                    == account.id
                )
                |
                (
                    Transaction.receiver_account_id
                    == account.id
                )
            ).delete(
                synchronize_session=False
            )

            db.session.delete(account)

        db.session.delete(user)
        db.session.commit()

        flash(
            "User deleted successfully.",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "The user could not be deleted.",
            "danger"
        )

    return redirect(
        url_for("admin.admin_dashboard")
    )