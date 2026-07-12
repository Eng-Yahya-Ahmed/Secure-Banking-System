from decimal import Decimal

from app.extensions import db
from app.models.user import User
from app.models.account import Account
from app.models.transactions import Transaction


PASSWORD = "TransferUser@12345"


def register_user(client, username, email):
    """
    تسجيل مستخدم جديد وإنشاء حسابه البنكي.
    """

    return client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": PASSWORD,
            "confirm_password": PASSWORD
        },
        follow_redirects=True
    )


def login_user(client, username):
    """
    تسجيل دخول مستخدم.
    """

    return client.post(
        "/login",
        data={
            "username": username,
            "password": PASSWORD
        },
        follow_redirects=True
    )


def get_account(app, username):
    """
    الحصول على حساب المستخدم من قاعدة البيانات.
    """

    with app.app_context():

        user = User.query.filter_by(
            username=username
        ).first()

        assert user is not None

        account = Account.query.filter_by(
            user_id=user.id
        ).first()

        assert account is not None

        return {
            "id": account.id,
            "account_number": account.account_number,
            "balance": Decimal(account.balance)
        }


def transfer_money(client, receiver_account_number, amount):
    """
    إرسال طلب تحويل.

    تمت إضافة عدة أسماء للحقل حتى يتوافق
    الاختبار مع اسم الحقل المستخدم في المشروع.
    """

    return client.post(
        "/transfer",
        data={
            "receiver_account_number": receiver_account_number,
            "recipient_account_number": receiver_account_number,
            "account_number": receiver_account_number,
            "receiver_account": receiver_account_number,
            "recipient_account": receiver_account_number,
            "amount": amount
        },
        follow_redirects=True
    )


def prepare_two_users(client, app):
    """
    إنشاء مستخدم مرسل ومستخدم مستلم.
    """

    register_user(
        client,
        username="senderuser",
        email="sender@gmail.com"
    )

    register_user(
        client,
        username="receiveruser",
        email="receiver@gmail.com"
    )

    sender_account = get_account(
        app,
        "senderuser"
    )

    receiver_account = get_account(
        app,
        "receiveruser"
    )

    login_user(
        client,
        "senderuser"
    )

    return sender_account, receiver_account


def test_successful_transfer_updates_balances(client, app):
    """
    التأكد من نجاح التحويل وتحديث الرصيدين.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        receiver["account_number"],
        "100.00"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        updated_receiver = db.session.get(
            Account,
            receiver["id"]
        )

        assert updated_sender is not None
        assert updated_receiver is not None

        assert Decimal(updated_sender.balance) == Decimal("900.00")
        assert Decimal(updated_receiver.balance) == Decimal("1100.00")

        transaction = Transaction.query.first()

        assert transaction is not None
        assert transaction.sender_account_id == sender["id"]
        assert transaction.receiver_account_id == receiver["id"]
        assert Decimal(transaction.amount) == Decimal("100.00")


def test_transfer_to_same_account_is_rejected(client, app):
    """
    منع التحويل إلى الحساب نفسه.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        sender["account_number"],
        "100.00"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )
        assert updated_sender is not None
        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0


def test_insufficient_balance_is_rejected(client, app):
    """
    منع تحويل مبلغ أكبر من الرصيد.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        receiver["account_number"],
        "5000.00"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        updated_receiver = db.session.get(
            Account,
            receiver["id"]
        )

        assert updated_sender is not None
        assert updated_receiver is not None

        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Decimal(updated_receiver.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0


def test_negative_amount_is_rejected(client, app):
    """
    منع المبلغ السالب.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        receiver["account_number"],
        "-50.00"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        assert updated_sender is not None
        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0


def test_zero_amount_is_rejected(client, app):
    """
    منع تحويل مبلغ يساوي صفرًا.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        receiver["account_number"],
        "0"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        assert updated_sender is not None
        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0


def test_unknown_receiver_account_is_rejected(client, app):
    """
    منع التحويل إلى رقم حساب غير موجود.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        "AAAAAAAAAAAA",
        "100.00"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        assert updated_sender is not None
        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0


def test_amount_with_more_than_two_decimals_is_rejected(client, app):
    """
    منع المبلغ الذي يحتوي أكثر من منزلتين عشريتين.
    """

    sender, receiver = prepare_two_users(
        client,
        app
    )

    response = transfer_money(
        client,
        receiver["account_number"],
        "10.123"
    )

    assert response.status_code == 200

    with app.app_context():

        updated_sender = db.session.get(
            Account,
            sender["id"]
        )

        assert updated_sender is not None
        assert Decimal(updated_sender.balance) == Decimal("1000.00")
        assert Transaction.query.count() == 0