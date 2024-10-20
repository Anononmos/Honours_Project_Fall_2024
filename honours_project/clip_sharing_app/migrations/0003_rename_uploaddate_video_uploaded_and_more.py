# Generated by Django 5.0.6 on 2024-09-23 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0002_alter_video_uploaddate_alter_videoinstance_expires_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='uploadDate',
            new_name='uploaded',
        ),
        migrations.AlterField(
            model_name='videoinstance',
            name='id',
            field=models.CharField(default='lNiUwb', help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False),
        ),
    ]