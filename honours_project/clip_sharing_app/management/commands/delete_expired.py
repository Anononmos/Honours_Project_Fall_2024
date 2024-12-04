from django.core.management import BaseCommand
from django.utils import timezone
from clip_sharing_app.models import Video

class Command(BaseCommand):
    help = 'Deletes Video and VideoInstance objects from the database that are expired.'

    def handle(self, *args, **options):
        expired_videos = Video.objects.filter(expires__lte=timezone.now())

        for video in expired_videos:
            self.stdout.write(
                f'Deleted Video:'
                f'\n\tid: {video.id},'
                f'\n\ttitle: {video.title},'
                f'\n\tuplaoded: {video.uploaded},'
                f'\n\texpires: {video.expires},'
                f'\n\ttime: {timezone.now()}\n'
            )
            
            video.delete()

        self.stdout('Successfully deleted all expired videos.')