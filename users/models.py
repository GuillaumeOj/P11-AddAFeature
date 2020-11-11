from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Favorite

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name=None, password=None):
        if not email:
            raise ValueError("The given email must be set")
        if not first_name:
            raise ValueError("The given first name must be set")
        if not password:
            raise ValueError("The given password must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name)
        user.set_password(password)

        user.is_staff = False
        user.is_superuser = False
        user.last_name = last_name

        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name=None, password=None):
        user = self.create_user(email, first_name, last_name, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractUser):
    """Custom user identified by email."""

    # See https://code.djangoproject.com/ticket/25313
    db_table = "auth_user"

    username = None

    # Required fields
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)

    # Optional fields
    last_name = models.CharField(_("last name"), max_length=150, blank=True, default="")

    # ManyToManyField
    favorites = models.ManyToManyField(Favorite)

    # Permissions
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email
