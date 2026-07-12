from decimal import Decimal

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

from app.extensions import db, limiter
from app.models.account import Account
from app.models.transactions import Transaction

from app.security.validation import (
    validate_account_number,
    validate_amount
)


transfer_bp = Blueprint(
    "transfer",
    __name__
)


@transfer_bp.route(
    "/transfer",
    methods=["GET", "POST"]
)
@login_required
@limiter.limit(
    "10 per minute",
    methods=["POST"],
    error_message=(
        "Too many transfer attempts. "
        "Please try again later."
    )
)
def transfer():
    """تنفيذ عملية تحويل مالية."""

    sender_account = Account.query.filter_by(
        user_id=current_user.id
    ).first()

    if sender_account is None:
        flash(
            (
                "No bank account is associated "
                "with your user account."
            ),
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        receiver_account_number = (
            request.form.get(
                "receiver_account_number"
            )
            or request.form.get(
                "recipient_account_number"
            )
            or request.form.get(
                "account_number"
            )
            or request.form.get(
                "receiver_account"
            )
            or request.form.get(
                "recipient_account"
            )
            or ""
        ).strip().upper()

        amount_text = request.form.get(
            "amount",
            ""
        ).strip()

        # هذه الدالة ترجع قيمتين.
        account_is_valid, account_error = (
            validate_account_number(
                receiver_account_number
            )
        )

        if not account_is_valid:
            flash(
                account_error,
                "danger"
            )

            return render_template(
                "transfer.html",
                account=sender_account
            )

        # هذه الدالة ترجع ثلاث قيم.
        amount_is_valid, amount_error, amount = (
            validate_amount(amount_text)
        )

        if not amount_is_valid or amount is None:
            flash(
                amount_error,
                "danger"
            )

            return render_template(
                "transfer.html",
                account=sender_account
            )

        receiver_account = Account.query.filter_by(
            account_number=receiver_account_number
        ).first()

        if receiver_account is None:
            flash(
                "Receiver account not found.",
                "danger"
            )

            return render_template(
                "transfer.html",
                account=sender_account
            )

        if receiver_account.id == sender_account.id:
            flash(
                (
                    "You cannot transfer money "
                    "to your own account."
                ),
                "danger"
            )

            return render_template(
                "transfer.html",
                account=sender_account
            )

        sender_balance = Decimal(
            str(sender_account.balance)
        )

        receiver_balance = Decimal(
            str(receiver_account.balance)
        )

        if amount > sender_balance:
            flash(
                "Insufficient balance.",
                "danger"
            )

            return render_template(
                "transfer.html",
                account=sender_account
            )

        try:
            sender_account.balance = (
                sender_balance - amount
            )

            receiver_account.balance = (
                receiver_balance + amount
            )

            # إنشاء سجل التحويل دون معاملات constructor.
            new_transaction = Transaction()
            new_transaction.sender_account_id = (
                sender_account.id
            )

            new_transaction.receiver_account_id = (
                receiver_account.id
            )

            new_transaction.amount = amount

            db.session.add(new_transaction)
            db.session.commit()

            flash(
                (
                    f"Transfer of ${amount:.2f} "
                    "completed successfully."
                ),
                "success"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        except Exception:
            db.session.rollback()

            flash(
                (
                    "The transfer could not be completed. "
                    "Please try again."
                ),
                "danger"
            )

    return render_template(
        "transfer.html",
        account=sender_account
    )  