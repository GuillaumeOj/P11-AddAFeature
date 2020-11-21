import os

from dotenv import find_dotenv, load_dotenv

from .base import *  # noqa: F401, F403

ALLOWED_HOSTS = ["*"]

load_dotenv(find_dotenv(filename=".env-local"))

SENDGRID_APY_KEY = os.getenv("SENDGRID_APY_KEY")

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
