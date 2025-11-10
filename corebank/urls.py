"""Routes."""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from corebank.api.views import RegisterView, LoginView, LogoutView,     BalanceView, TransactionsView, TransferView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="docs"),
    path("api/v1/auth/register", RegisterView.as_view(), name="register"),
    path("api/v1/auth/login", LoginView.as_view(), name="login"),
    path("api/v1/auth/logout", LogoutView.as_view(), name="logout"),
    path("api/v1/accounts/balance", BalanceView.as_view(), name="balance"),
    path("api/v1/accounts/transactions", TransactionsView.as_view(),
         name="transactions"),
    path("api/v1/accounts/transfer", TransferView.as_view(), name="transfer"),
]
