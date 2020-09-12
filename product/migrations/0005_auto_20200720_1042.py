# Generated by Django 3.0.8 on 2020-07-20 08:42

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_auto_20200712_1325"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="fat_100",
            field=models.DecimalField(
                blank=True, decimal_places=3, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="salt_100",
            field=models.DecimalField(
                blank=True, decimal_places=3, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="saturated_fat_100",
            field=models.DecimalField(
                blank=True, decimal_places=3, default=0, max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="sugar_100",
            field=models.DecimalField(
                blank=True, decimal_places=3, default=0, max_digits=6
            ),
        ),
    ]
