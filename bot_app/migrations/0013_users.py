# Generated by Django 4.0.3 on 2022-03-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0012_delete_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('chat_id', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
    ]