from django.core.management import BaseCommand
from clip_sharing_app.models import delete_expired

class Command(BaseCommand):
    help = 'Deletes Video and VideoInstance objects from the database that are expired.'

    def handle(self, *args, **options):
        delete_expired()

        self.stdout.write('Successfully deleted all expired videos.')