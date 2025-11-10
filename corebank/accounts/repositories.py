from decimal import Decimal
from typing import Optional
from django.db import transaction
from corebank.models import Account, Transaction
def create_account(*, owner_kc_id: str, account_number: str, currency: str,
                   commission_rate: Decimal) -> Account:
    return Account.objects.create(
        owner_kc_id=owner_kc_id, account_number=account_number,
        currency=currency, commission_rate=commission_rate
    )
def get_account_by_owner(owner_kc_id: str) -> Optional[Account]:
    return Account.objects.filter(owner_kc_id=owner_kc_id).first()
def get_account_by_number(account_number: str) -> Optional[Account]:
    return Account.objects.filter(account_number=account_number).first()
@transaction.atomic
def post_transaction(account: Account, amount: Decimal, is_credit: bool
                     ) -> Transaction:
    txn = Transaction.objects.create(
        account=account, amount=amount,
        type=Transaction.CREDIT if is_credit else Transaction.DEBIT
    )
    account.amount = account.amount + amount if is_credit         else account.amount - amount
    account.save(update_fields=["amount"])
    return txn
def list_transactions_for_owner(owner_kc_id: str, date_from, date_to):
    qs = Transaction.objects.filter(account__owner_kc_id=owner_kc_id)
    if date_from: qs = qs.filter(created_at__date__gte=date_from)
    if date_to: qs = qs.filter(created_at__date__lte=date_to)
    return list(qs.order_by("-created_at"))
