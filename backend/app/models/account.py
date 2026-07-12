from datetime import datetime
from decimal import Decimal

from app.extensions import db


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    account_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    balance = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=Decimal("1000.00")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="account"
    )

    def repr(self):
        return f"<Account {self.account_number}>"