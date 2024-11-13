import os
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

# Create your models here.

# Get the expiration time

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(env_path)

EXPIRY = int( os.environ.get('EXPIRY') )    # In minutes

def upload_to(instance, filename):
    """Saves file as {video_id}.{extension}."""

    extension = filename.split('.')[-1] 

    return f'uploads/{instance.video.id}.{extension}'


class Video(models.Model):
    """Includes video information i.e., title, upload-date, etc."""

    id = models.CharField( 
        primary_key=True, 
        unique=True, 
        max_length=6, 
        help_text='6-character alphanumeric id for video.' 
    )

    uploaded = models.DateTimeField( 
        auto_now_add=True, 
        help_text='Upload date for the video.' 
    )
    expires = models.DateTimeField( 
        null=True, 
        help_text='Expiry time of the video.' 
    )

    title = models.CharField( 
        max_length=50, 
        blank=True, 
        null=True, 
        help_text='Enter a title for the video.' 
    )

    views = models.PositiveIntegerField( 
        default=0, 
        help_text='Share count of the video.' 
    )

    def delete(self):
        """Clears the view count from the cache when the video is deleted."""

        cache.delete(self.id)
        return super(Video, self).delete()


    def save(self, *args, **kwargs):
        """
        Saves the video object to the database. 
        Creates 6-character alphanumeric id for the database entry. 
        Creates an expiration date 10 minutes after upload.
        """

        if not self.id:
            self.id = get_random_string(length=6)

        if not self.expires:
            self.expires = timezone.now() + timedelta(minutes=EXPIRY)

        return super(Video, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return f'id: {self.id}, title: {self.title}'


class VideoInstance(models.Model):
    """Includes video file and video info as separate object."""

    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)
    

    def delete(self):
        """Deletes the uploaded file when the instance is deleted."""

        self.file.delete()
        super(VideoInstance, self).delete()

        return
    
    # Admin display functions
    # Displays fields on the Admin site

    def get_id(self):
        return self.video.id
    
    def get_expiry(self):
        return self.video.expires

    def get_uploaded(self):
        return self.video.uploaded

    def get_title(self):
        return self.video.title
    
    def get_views(self):
        return self.video.views
    
    get_id.short_description = 'Id'
    get_expiry.short_description = 'Expiry Date'
    get_uploaded.short_description = 'Upload Date'
    get_title.short_description = 'Title'
    get_views.short_description = 'View Count'

    def __str__(self) -> str:
        return f'VideoInstance, filename: {self.file.name}, info: {self.video}'
    

# File delete functions

def delete_expired():
    """Deletes expired videos. Meant to be executed daily."""

    expired_videos = Video.objects.filter(expires__lte=timezone.now())
    
    for video in expired_videos:
        video.delete()


def _delete_file(path):
    """Deletes file from filesystem"""

    if os.path.isfile(path):
        os.remove(path)

    return


@receiver(models.signals.post_delete, sender=VideoInstance)
def delete_file(sender, instance, *args, **kwargs):
    """Deletes associated video file when VideoInstance object is deleted."""

    if instance.file: 
        _delete_file(instance.file.path)

    return