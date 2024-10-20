import os
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

EXPIRY = 10     # In minutes

def upload_to(instance, filename):
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
        help_text='View count of the video.' 
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_random_string(length=6)

        if not self.expires:
            self.expires = timezone.now() + timedelta(minutes=EXPIRY)

        return super(Video, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'id: {self.id}, title: {self.title}'


class VideoInstance(models.Model):
    """Includes video file and access code."""

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
    get_views.short_description = 'Viewcount'

    def __str__(self) -> str:
        return f'VideoInstance, filename: {self.file.name}, info: {self.video}'
    

# File delete functions

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