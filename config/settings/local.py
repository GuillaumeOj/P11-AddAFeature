"""Django settings for the local project."""
import os

from dotenv import find_dotenv
from dotenv import load_dotenv

from .base import *


ALLOWED_HOSTS = ["*"]

load_dotenv(find_dotenv(filename=".env-local"))
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True if os.getenv("DEBUG") == "True" else False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
    }
}
