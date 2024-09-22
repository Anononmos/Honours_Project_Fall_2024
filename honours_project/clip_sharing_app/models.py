from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

# Create your models here.

class Video(models.Model):
    """Includes video information i.e., title, upload-date, etc."""

    title = models.CharField(max_length=50, blank=True, null=True, help_text='Enter a title for the video.')
    views = models.PositiveIntegerField(default=0, help_text='View count of the video.')
    uploadDate = models.DateTimeField(editable=False, help_text='Upload date for the video.')

    def __str__(self) -> str:
        return f'Title: {self.title}\nUploaded: {self.uploadDate}\n {self.views} views.'


class VideoInstance(models.Model):
    """Includes video file and access code."""

    id = models.CharField(primary_key=True, max_length=6, default=get_random_string(length=6), editable=False, help_text='6-character alphanumeric id for video.')
    expires = models.DateTimeField(editable=False, help_text='Expiry time of the video.')
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")

    def __str__(self) -> str:
        return f'Id: {self.id}\nInfo: ({self.video})'