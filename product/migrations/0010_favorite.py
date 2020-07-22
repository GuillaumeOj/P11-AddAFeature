# Generated by Django 3.0.8 on 2020-07-21 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20200721_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to='product.Product')),
                ('substitute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_substitute', to='product.Product')),
            ],
        ),
    ]
