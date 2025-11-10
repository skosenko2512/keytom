from typing import Optional
from django.conf import settings
from django.http import HttpRequest
import requests


def get_owner_kc_id(request: HttpRequest) -> Optional[str]:
    """
    Возвращает ID пользователя по access-токену Keycloak.
    В dev-режиме допускает X-User-KC-ID.
    """
    if settings.DEBUG:
        return request.headers.get("X-User-KC-ID")

    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None

    token = auth.removeprefix("Bearer ").strip()
    try:
        resp = requests.get(
            f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("sub") or data.get("preferred_username")
    except requests.RequestException:
        return None

    return None
