# Generated by Django 4.0.3 on 2022-03-10 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0011_users'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]