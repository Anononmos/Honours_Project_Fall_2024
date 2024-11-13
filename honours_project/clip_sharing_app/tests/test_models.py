from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from ..models import Video, VideoInstance, delete_expired
import time

EXPIRY = 10 # In minutes

class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        video: Video = Video.objects.create(title="video-test")
        cls.id: str = video.id
    

    def setUp(self):
        # Run once for every test method to set up clean data.

        ...


    def test_expiry(self):
        """
        Test if the video object's expiry date is initialized to 10 minutes after its upload date.
        """

        # TODO: On pythonanywhere, this fails because datetime.timedelta cannot be rounded.

        video: Video = Video.objects.get(id=self.id)
        one_second = timedelta(minutes=EXPIRY, seconds=1)
        difference = video.expires - video.uploaded

        self.assertTrue(difference < one_second, msg=f'Time difference between the upload date and expiry date is {difference}.')

    
    def test_title(self):
        """
        Test if video title is saved including quotes, inequalities and colons.
        """

        title = '"\'?><:;* a%'
        video = Video.objects.create(title=title)

        self.assertEqual(video.title, title)

    
    def test_empty_title(self):
        """
        Test if video object accepts empty title.
        """

        video = Video.objects.create(title='')

        self.assertEqual(video.title, '')


    def test_expired_video_delete(self):
        """Test if calling delete_expired deletes only expired videos."""

        # Create and save videos that are expired.

        expired_videos: list[str] = []
        videos: list[str] = []

        # create expired videos

        for _ in range(10):
            video = Video.objects.create()
            video.expires = timezone.now()  # Set expiry date to current time
            video.save()

            expired_videos.append(video.id)

        # Create normal videos

        for _ in range(10):
            video = Video.objects.create()
            video.save()

            videos.append(video.id)

        time.sleep(1)   # Sleep for one second.
        
        delete_expired()

        for i in range(10):
            id = videos[i]
            exp_id = expired_videos[i]

            exp_exists = Video.objects.filter(id=exp_id).exists()
            vid_exists = Video.objects.filter(id=id).exists()

            self.assertFalse(exp_exists, msg=f'Expired video with id {exp_id} exists in database.')
            self.assertTrue(vid_exists, msg=f'Video with id {id} does not exist in database.')

        return


class VideoInstanceModelTest(TestCase):
    ...
    