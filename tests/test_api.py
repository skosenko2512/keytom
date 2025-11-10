import json
from django.urls import reverse
from corebank.accounts.services import ensure_user_account, apply_welcome_bonus
def test_register(api_client, db):
    r = api_client.post(reverse("register"),
                        data=json.dumps({"email":"a@b.c","password":"Xx123"}),
                        content_type="application/json")
    assert r.status_code == 200 and "user_id" in r.json()
def test_balance(api_client, db):
    ensure_user_account("kc-1"); apply_welcome_bonus("kc-1")
    r = api_client.get(reverse("balance"))
    assert r.status_code == 200 and r.json()["amount"] == "10000.00"
def test_transfer(api_client, db):
    from corebank.accounts.repositories import get_account_by_owner
    ensure_user_account("kc-1"); apply_welcome_bonus("kc-1")
    ensure_user_account("kc-2"); a2 = get_account_by_owner("kc-2").account_number
    r = api_client.post(reverse("transfer"),
                        data=json.dumps({"to_account_number":a2,"amount":"100.00"}),
                        content_type="application/json")
    assert r.status_code == 200 and r.json()["detail"] == "ok"
