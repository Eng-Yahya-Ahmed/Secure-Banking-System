from datetime import datetime
from decimal import Decimal

from app.extensions import db


class Transaction(db.Model):

    tablename = "transactions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False,
        index=True
    )

    receiver_account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False,
        index=True
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    sender_account = db.relationship(
        "Account",
        foreign_keys=[sender_account_id]
    )

    receiver_account = db.relationship(
        "Account",
        foreign_keys=[receiver_account_id]
    )

    def repr(self):
        return (
            f"<Transaction "
            f"id={self.id}, "
            f"sender={self.sender_account_id}, "
            f"receiver={self.receiver_account_id}, "
            f"amount={self.amount}>"
        )

    def is_valid_amount(self):
        return (
            self.amount is not None
            and Decimal(self.amount) > Decimal("0.00")
        )