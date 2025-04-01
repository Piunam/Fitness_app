# Generated by Django 5.1.3 on 2025-04-01 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='date',
        ),
        migrations.AddField(
            model_name='workout',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 4, 1, 19, 6, 29, 721103)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='duration',
            field=models.IntegerField(default=30, help_text='Duration in minutes'),
            preserve_default=False,
        ),
    ]
