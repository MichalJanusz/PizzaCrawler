# Generated by Django 3.0.2 on 2020-01-25 20:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crawler', '0003_auto_20200125_2130'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserExtension',
            new_name='UserInfo',
        ),
    ]
