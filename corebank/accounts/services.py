import random
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from corebank.accounts.repositories import (
    create_account, get_account_by_number, get_account_by_owner,
    post_transaction,
)
def _gen_account_number() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(10))
def ensure_user_account(owner_kc_id: str) -> str:
    acc = get_account_by_owner(owner_kc_id)
    if acc: return acc.account_number
    acc_number = _gen_account_number()
    create_account(owner_kc_id=owner_kc_id, account_number=acc_number,
                   currency=settings.CURRENCY_DEFAULT,
                   commission_rate=Decimal(str(settings.DEFAULT_COMMISSION_RATE)))
    return acc_number
def apply_welcome_bonus(owner_kc_id: str) -> None:
    acc = get_account_by_owner(owner_kc_id)
    if not acc:
        acc_number = ensure_user_account(owner_kc_id)
        acc = get_account_by_number(acc_number)
    post_transaction(acc, Decimal(settings.WELCOME_BONUS), is_credit=True)
def _calc_commission(amount: Decimal, currency: str, rate: Decimal) -> Decimal:
    if currency == "EUR" and amount <= Decimal(settings.MIN_COMMISSION_THRESHOLD_EUR):
        return Decimal(settings.MIN_COMMISSION_EUR)
    val = (amount * rate / Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP)
    if currency == "EUR" and val < Decimal(settings.MIN_COMMISSION_EUR):
        return Decimal(settings.MIN_COMMISSION_EUR)
    return val
def transfer(owner_kc_id: str, to_account_number: str, amount: Decimal) -> None:
    if amount <= 0: raise ValueError("Amount must be positive.")
    sender = get_account_by_owner(owner_kc_id)
    if not sender: raise ValueError("Sender account not found.")
    receiver = get_account_by_number(to_account_number)
    if not receiver: raise ValueError("Receiver account not found.")
    commission = _calc_commission(amount, sender.currency, sender.commission_rate)
    total_debit = amount + commission
    if sender.amount < total_debit: raise ValueError("Insufficient funds.")
    post_transaction(sender, total_debit, is_credit=False)
    post_transaction(receiver, amount, is_credit=True)
