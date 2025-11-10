from decimal import Decimal
from corebank.accounts.services import ensure_user_account, apply_welcome_bonus, transfer
from corebank.accounts.repositories import get_account_by_owner
def test_bonus_flow(db):
    ensure_user_account("kc-1"); apply_welcome_bonus("kc-1")
    acc = get_account_by_owner("kc-1")
    assert str(acc.amount) == "10000.00"
def test_commission_minimum(db):
    ensure_user_account("kc-1"); ensure_user_account("kc-2")
    apply_welcome_bonus("kc-1")
    transfer("kc-1", get_account_by_owner("kc-2").account_number, Decimal("100.00"))
    s = get_account_by_owner("kc-1"); r = get_account_by_owner("kc-2")
    s.refresh_from_db(); r.refresh_from_db()
    assert str(s.amount) == "9895.00" and str(r.amount) == "100.00"
def test_commission_percent(db):
    ensure_user_account("kc-1"); ensure_user_account("kc-2")
    apply_welcome_bonus("kc-1")
    transfer("kc-1", get_account_by_owner("kc-2").account_number, Decimal("1000.00"))
    s = get_account_by_owner("kc-1"); r = get_account_by_owner("kc-2")
    s.refresh_from_db(); r.refresh_from_db()
    assert str(s.amount) == "8975.00" and str(r.amount) == "1000.00"
