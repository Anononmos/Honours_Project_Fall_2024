# Generated by Django 5.0.6 on 2024-09-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0007_remove_videoinstance_expires_video_expires_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(default='fmVAcN', help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False),
        ),
    ]
