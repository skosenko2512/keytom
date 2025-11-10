import os, requests
class KeycloakClient:
    def __init__(self) -> None:
        self.base = os.getenv("KEYCLOAK_URL","").rstrip("/")
        self.realm = os.getenv("KEYCLOAK_REALM","")
        self.client_id = os.getenv("KEYCLOAK_CLIENT_ID","")
        self.client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET","")
    def available(self) -> bool:
        return bool(self.base and self.realm and self.client_id)
    def issue_token(self, username: str, password: str) -> dict:
        url = f"{self.base}/realms/{self.realm}/protocol/openid-connect/token"
        data = {"grant_type":"password","client_id":self.client_id,
                "client_secret":self.client_secret,
                "username":username,"password":password}
        r = requests.post(url, data=data, timeout=10); r.raise_for_status()
        return r.json()
    def logout(self, refresh_token: str) -> None:
        url = f"{self.base}/realms/{self.realm}/protocol/openid-connect/logout"
        data = {"client_id":self.client_id,"client_secret":self.client_secret,
                "refresh_token":refresh_token}
        r = requests.post(url, data=data, timeout=10); r.raise_for_status()
