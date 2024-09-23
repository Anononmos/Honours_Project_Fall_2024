# Generated by Django 5.0.6 on 2024-09-23 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='uploadDate',
            field=models.DateTimeField(auto_now_add=True, help_text='Upload date for the video.'),
        ),
        migrations.AlterField(
            model_name='videoinstance',
            name='expires',
            field=models.DateTimeField(help_text='Expiry time of the video.'),
        ),
        migrations.AlterField(
            model_name='videoinstance',
            name='id',
            field=models.CharField(default='ZbD1bP', help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False),
        ),
    ]