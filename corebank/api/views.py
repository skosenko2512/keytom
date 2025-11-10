import json, asyncio
from datetime import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from corebank.models import UserProfile
from corebank.users.keycloak import KeycloakClient
from corebank.users.publisher import publish_user_created
from corebank.accounts.repositories import get_account_by_owner,     list_transactions_for_owner
from corebank.accounts.services import transfer, ensure_user_account,     apply_welcome_bonus
from .authz import get_owner_kc_id
from .serializers import TransferSerializer
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body or b"{}")
        email = data.get("email"); password = data.get("password")
        if not email or not password:
            return JsonResponse({"detail":"email/password required"}, status=400)
        kc = KeycloakClient()
        kc_id = email if kc.available() else f"kc-{abs(hash(email))%10_000_000}"
        UserProfile.objects.get_or_create(
            email=email, defaults={"keycloak_user_id": kc_id})
        ensure_user_account(kc_id)
        asyncio.run(publish_user_created(kc_id))
        return JsonResponse({"user_id": kc_id})
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body or b"{}")
        email = data.get("email"); password = data.get("password")
        if not email or not password:
            return JsonResponse({"detail":"email/password required"}, status=400)
        kc = KeycloakClient()
        if kc.available():
            try:
                tok = kc.issue_token(email, password)
                return JsonResponse({"access_token":tok.get("access_token"),
                                     "refresh_token":tok.get("refresh_token")})
            except Exception as exc:
                return JsonResponse({"detail":str(exc)}, status=400)
        return JsonResponse({"access_token":f"dev-{email}",
                             "refresh_token":f"dev-refresh-{email}"})
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body or b"{}")
        token = data.get("refresh_token")
        kc = KeycloakClient()
        if kc.available() and token:
            try: kc.logout(token)
            except Exception as exc: return JsonResponse({"detail":str(exc)},400)
        return JsonResponse({"detail":"ok"})
class BalanceView(APIView):
    def get(self, request, *args, **kwargs):
        owner = get_owner_kc_id(request)
        if not owner: return JsonResponse({"detail":"unauthorized"}, 401)
        acc = get_account_by_owner(owner)
        if not acc: return JsonResponse({"amount":"0.00","currency":"EUR"})
        return JsonResponse({"amount":str(acc.amount), "currency":acc.currency})
class TransactionsView(APIView):
    def get(self, request, *args, **kwargs):
        owner = get_owner_kc_id(request)
        if not owner: return JsonResponse({"detail":"unauthorized"}, 401)
        dfrom = request.GET.get("from"); dto = request.GET.get("to")
        date_from = datetime.fromisoformat(dfrom).date() if dfrom else None
        date_to = datetime.fromisoformat(dto).date() if dto else None
        txns = list_transactions_for_owner(owner, date_from, date_to)
        data = [{"id":str(t.id),"amount":str(t.amount),"type":t.type,
                 "created_at":t.created_at.isoformat()} for t in txns]
        return JsonResponse({"transactions": data})
class TransferView(APIView):
    def post(self, request, *args, **kwargs):
        owner = get_owner_kc_id(request)
        if not owner: return JsonResponse({"detail":"unauthorized"}, 401)
        ser = TransferSerializer(data=request.data); ser.is_valid(raise_exception=True)
        try:
            transfer(owner, ser.validated_data["to_account_number"],
                     ser.validated_data["amount"])
        except ValueError as e:
            return JsonResponse({"detail":str(e)}, status=400)
        return JsonResponse({"detail":"ok"})
