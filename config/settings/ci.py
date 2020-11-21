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
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_NAME", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default=""),
        "HOST": os.getenv("POSTGRES_HOST", default=""),
        "PORT": os.getenv("POSTGRES_PORT", default=""),
    }
}
