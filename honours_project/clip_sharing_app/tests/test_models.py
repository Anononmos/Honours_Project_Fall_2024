from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from ..models import Video, VideoInstance

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

        video: Video = Video.objects.get(id=self.id)
        ten_minutes = timedelta(minutes=EXPIRY)
        difference = video.expires - video.uploaded

        self.assertAlmostEqual(difference, ten_minutes, places=0, msg=f'Time difference between the upload date and expiry date is {difference}.')

    
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


class VideoInstanceModelTest(TestCase):
    ...