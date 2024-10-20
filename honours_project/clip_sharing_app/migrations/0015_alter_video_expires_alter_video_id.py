# Generated by Django 5.0.6 on 2024-10-12 02:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0014_alter_video_expires_alter_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 12, 3, 4, 55, 117114, tzinfo=datetime.timezone.utc), help_text='Expiry time of the video.'),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]