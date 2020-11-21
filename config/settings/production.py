import os

import sentry_sdk
from dotenv import find_dotenv, load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F401, F403

ALLOWED_HOSTS = [
    "projet-11.ojardias.io",
]

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True if os.getenv("DEBUG") == "True" else False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

# Enable sentry
sentry_sdk.init(
    dsn="https://947b8a21015b4d91a53a9ca93a99852f@o453278.ingest.sentry.io/5500766",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# Settings for email client
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True if os.getenv("EMAIL_USE_SSL") else False
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
