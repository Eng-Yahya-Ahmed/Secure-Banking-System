from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.account import Account
from app.models.transactions import Transaction


transactions_bp = Blueprint(
    "transactions",
    __name__
)


@transactions_bp.route("/transactions")
@login_required
def transactions():

    account = Account.query.filter_by(
        user_id=current_user.id
    ).first()

    if account is None:
        return render_template(
            "transactions.html",
            account=None,
            transactions=[]
        )

    user_transactions = Transaction.query.filter(
        (
            Transaction.sender_account_id
            == account.id
        )
        |
        (
            Transaction.receiver_account_id
            == account.id
        )
    ).order_by(
        Transaction.created_at.desc()
    ).all()

    return render_template(
        "transactions.html",
        account=account,
        transactions=user_transactions
    )