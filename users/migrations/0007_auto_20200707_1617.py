# Generated by Django 3.0.8 on 2020-07-07 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('admin', '0004_auto_20200707_1611'),
        ('users', '0006_auto_20200707_1611'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='User',
        ),
    ]
