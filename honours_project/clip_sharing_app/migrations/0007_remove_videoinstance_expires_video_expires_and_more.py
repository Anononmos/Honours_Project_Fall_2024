# Generated by Django 5.0.6 on 2024-09-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0006_alter_videoinstance_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoinstance',
            name='expires',
        ),
        migrations.AddField(
            model_name='video',
            name='expires',
            field=models.DateTimeField(help_text='Expiry time of the video.', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(default='aqfzrB', help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='videoinstance',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
