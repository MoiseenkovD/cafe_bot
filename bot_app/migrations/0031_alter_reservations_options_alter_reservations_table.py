# Generated by Django 4.0.3 on 2022-03-12 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0030_reservations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservations',
            options={'verbose_name': 'reservations', 'verbose_name_plural': 'Reservations'},
        ),
        migrations.AlterModelTable(
            name='reservations',
            table='reservations',
        ),
    ]
