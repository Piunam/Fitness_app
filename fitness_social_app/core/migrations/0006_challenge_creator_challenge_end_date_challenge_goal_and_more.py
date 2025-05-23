# Generated by Django 5.1.3 on 2025-04-02 09:11

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_challenge_achievement_challengeparticipation_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_challenges', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challenge',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='goal',
            field=models.IntegerField(default=10, help_text='Target number of workouts to complete'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challengeparticipation',
            name='joined_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 4, 2, 9, 11, 43, 503383, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='challengeparticipation',
            unique_together={('user', 'challenge')},
        ),
    ]
