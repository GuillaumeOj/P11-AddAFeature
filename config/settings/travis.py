import os

from dotenv import find_dotenv
from dotenv import load_dotenv

from .base import *  # noqa: F401, F403


ALLOWED_HOSTS = ["*"]

load_dotenv(find_dotenv(filename=".env-local"))

SECRET_KEY = os.getenv("SECRET_KEY", default="foo-key-for-travis")
DEBUG = True if os.getenv("DEBUG") == "True" else False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", default=""),
        "USER": os.getenv("DATABASE_USER", default="postgres"),
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

print(DATABASES)
