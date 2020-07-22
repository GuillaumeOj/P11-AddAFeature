# Generated by Django 3.0.8 on 2020-07-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20200720_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fat_100',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='salt_100',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='saturated_fat_100',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='sugars_100',
            field=models.FloatField(blank=True, default=0),
        ),
    ]