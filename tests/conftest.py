import pytest
from django.conf import settings
from django.test import Client
@pytest.fixture(autouse=True)
def _db_sqlite(monkeypatch: pytest.MonkeyPatch) -> None:
    settings.DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
    settings.DATABASES["default"]["NAME"] = ":memory:"
    monkeypatch.setenv("DJANGO_DEBUG", "True")
@pytest.fixture()
def api_client() -> Client:
    return Client(HTTP_X_USER_KC_ID="kc-1")
