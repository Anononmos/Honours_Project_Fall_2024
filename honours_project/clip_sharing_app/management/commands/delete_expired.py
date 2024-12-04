from django.core.management import BaseCommand
from django.utils import timezone
from clip_sharing_app.models import Video

class Command(BaseCommand):
    help = 'Deletes Video and VideoInstance objects from the database that are expired.'

    def handle(self, *args, **options):
        expired_videos = Video.objects.filter(expires__lte=timezone.now())

        for video in expired_videos:
            self.stdout(f'Deleted Video:\n\tid: {video.id},\ttitle: {video.title},\tuplaoded: {video.uploaded},\texpires: {video.expires},\ttime: {timezone.now()}\n')
            
            video.delete()

        self.stdout('Successfully deleted all expired videos.')