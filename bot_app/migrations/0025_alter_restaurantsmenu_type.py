# Generated by Django 4.0.3 on 2022-03-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0024_alter_restaurantsmenu_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantsmenu',
            name='type',
            field=models.CharField(choices=[(0, 'MENU'), (1, 'BAR')], default=0, max_length=10),
        ),
    ]
