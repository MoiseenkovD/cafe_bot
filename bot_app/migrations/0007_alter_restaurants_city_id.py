# Generated by Django 4.0.3 on 2022-03-08 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0006_rename_name_cities_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_app.cities', verbose_name='city'),
        ),
    ]
