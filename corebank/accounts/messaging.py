import json, asyncio
from django.conf import settings
from nats.aio.client import Client as NATS
from corebank.accounts.services import ensure_user_account, apply_welcome_bonus

async def _connect() -> NATS:
    nc = NATS(); await nc.connect(servers=[settings.NATS_URL]); return nc
async def start_consumers() -> None:
    nc = await _connect(); js = nc.jetstream()
    await js.add_stream({"name":settings.ACCOUNTS_STREAM,
                         "subjects":[settings.SUBJECT_USER_CREATED,
                                     settings.SUBJECT_BONUS_CREDIT]})
    async def on_user_created(msg):
        data = json.loads(msg.data.decode("utf-8"))
        owner_kc_id = data["user_id"]
        acc_number = ensure_user_account(owner_kc_id)
        await js.publish(settings.SUBJECT_BONUS_CREDIT, json.dumps({
            "user_id": owner_kc_id, "account_number": acc_number,
            "amount": settings.WELCOME_BONUS,
        }).encode("utf-8"))
    async def on_bonus_credit(msg):
        data = json.loads(msg.data.decode("utf-8"))
        apply_welcome_bonus(data.get("user_id"))
    await js.subscribe(settings.SUBJECT_USER_CREATED, cb=on_user_created)
    await js.subscribe(settings.SUBJECT_BONUS_CREDIT, cb=on_bonus_credit)
    try:
        while True: await asyncio.sleep(1)
    finally: await nc.drain()
