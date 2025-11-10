import json
from django.conf import settings
from nats.aio.client import Client as NATS
async def publish_user_created(user_id: str) -> None:
    nc = NATS(); await nc.connect(servers=[settings.NATS_URL])
    js = nc.jetstream()
    await js.add_stream({"name":settings.ACCOUNTS_STREAM,
                         "subjects":[settings.SUBJECT_USER_CREATED,
                                     settings.SUBJECT_BONUS_CREDIT]})
    await js.publish(settings.SUBJECT_USER_CREATED,
                     json.dumps({"user_id": user_id}).encode("utf-8"))
    await nc.drain()
