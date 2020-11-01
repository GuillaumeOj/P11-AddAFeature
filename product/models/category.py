from django.core.validators import MinLengthValidator
from django.db import models


class Category(models.Model):
    """Model for a Category for a Product."""

    name = models.CharField(
        unique=True,
        max_length=100,
        validators=[MinLengthValidator(2)],
    )

    def __str__(self):
        return self.name
