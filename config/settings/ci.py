import os

from dotenv import find_dotenv, load_dotenv

from .base import *  # noqa: F401, F403

ALLOWED_HOSTS = ["*"]

load_dotenv(find_dotenv(filename=".env-local"))

SECRET_KEY = os.getenv("SECRET_KEY", default="foo-key")

DEBUG = True if os.getenv("DEBUG") == "True" else False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", default=""),
        "USER": os.getenv("POSTGRES_USER", default=""),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default=""),
        "HOST": os.getenv("POSTGRES_HOST", default=""),
        "PORT": os.getenv("POSTGRES_PORT", default=""),
    }
}

# Settings for email client
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
