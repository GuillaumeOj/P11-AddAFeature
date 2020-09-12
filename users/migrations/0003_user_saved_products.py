# Generated by Django 3.0.8 on 2020-07-21 13:43

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0009_auto_20200721_1053"),
        ("users", "0002_auto_20200721_1536"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="saved_products",
            field=models.ManyToManyField(to="product.Product"),
        ),
    ]
