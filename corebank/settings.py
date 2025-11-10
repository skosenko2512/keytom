"""Single-app settings."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev")
DEBUG = os.getenv("DJANGO_DEBUG","False").lower()=="true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS","*").split(",")]
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages",
    "django.contrib.staticfiles","rest_framework","drf_spectacular",
    # only single app below
    "corebank",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "corebank.urls"
TEMPLATES = [{
    "BACKEND":"django.template.backends.django.DjangoTemplates",
    "DIRS":[], "APP_DIRS":True,
    "OPTIONS":{"context_processors":[
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "corebank.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE":"django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME","corebank_db"),
        "USER": os.getenv("DB_USER","corebank_user"),
        "PASSWORD": os.getenv("DB_PASSWORD","password"),
        "HOST": os.getenv("DB_HOST","localhost"),
        "PORT": os.getenv("DB_PORT","5432"),
    }
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
  "DEFAULT_RENDERER_CLASSES":["rest_framework.renderers.JSONRenderer"],
  "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {"TITLE":"CoreBank API","VERSION":"1.0.0"}
# NATS / Business
NATS_URL = os.getenv("NATS_URL","nats://localhost:4222")
ACCOUNTS_STREAM = os.getenv("ACCOUNTS_STREAM","accounts")
SUBJECT_USER_CREATED = os.getenv("SUBJECT_USER_CREATED","accounts.user.created")
SUBJECT_BONUS_CREDIT = os.getenv("SUBJECT_BONUS_CREDIT","accounts.bonus.credit")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL","")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM","")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID","")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET","")
CURRENCY_DEFAULT = os.getenv("CURRENCY_DEFAULT","EUR")
WELCOME_BONUS = int(os.getenv("WELCOME_BONUS","10000"))
MIN_COMMISSION_EUR = int(os.getenv("MIN_COMMISSION_EUR","5"))
MIN_COMMISSION_THRESHOLD_EUR = int(os.getenv("MIN_COMMISSION_THRESHOLD_EUR","200"))
DEFAULT_COMMISSION_RATE = float(os.getenv("DEFAULT_COMMISSION_RATE","2.5"))
