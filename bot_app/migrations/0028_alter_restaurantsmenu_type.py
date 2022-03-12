# Generated by Django 4.0.3 on 2022-03-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0027_alter_restaurantsmenu_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantsmenu',
            name='type',
            field=models.CharField(choices=[(1, 'MENU'), (2, 'BAR')], default=1, max_length=10),
        ),
    ]