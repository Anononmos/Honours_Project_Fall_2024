# Generated by Django 5.0.6 on 2024-09-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip_sharing_app', '0005_alter_videoinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinstance',
            name='id',
            field=models.CharField(default='enCS9G', help_text='6-character alphanumeric id for video.', max_length=6, primary_key=True, serialize=False),
        ),
    ]
