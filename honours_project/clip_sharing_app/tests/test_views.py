from django.test import TestCase, Client
from django.utils import timezone
from django.utils.crypto import get_random_string
from pathlib import Path
from ..models import Video, VideoInstance
from ..scripts import extract_id
import time

class UploadPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Initializes unchanging variables."""

        # Gets directory of testing files
        
        BASE_DIR = Path(__file__).resolve().parent / 'test_files'

        # Get paths of test video files

        cls.webm = BASE_DIR / 'webm_video.webm'
        cls.mp4 = BASE_DIR / 'mp4_video.mp4'

        cls.empty = BASE_DIR / 'empty_video.webm'
        cls.size_limit = BASE_DIR / 'over_50MB_video.webm'
        cls.time_limit = BASE_DIR / 'over_60s_video.mp4'
        cls.non_video = BASE_DIR / 'not_video.png'

    
    def setUp(self):
        """Initializes variables for each time a test is run."""


    def test_get_upload_page(self):
        """Tests sending a GET request to "/" and receiving "index.html" as a response."""

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200, msg=f'Get request to "/" responded with status code {response.status_code}.')
        self.assertTemplateUsed(response, 'index.html')

    # Test valid uploads

    def test_webm_upload(self):
        """Tests if sending a valid webm file as a POST request to "/" responds with 302 status code."""

        with open(self.webm, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

        try:
            self.assertEqual(res.status_code, 302)
            self.assertTrue(res.url.startswith('/watch'))

        except Exception as err:
            raise err

        finally:
            # Delete uploaded file
            # Get param that comes after "v="

            video_id = extract_id(res.url)    
            Video.objects.get(id=video_id).delete()


    def test_mp4_upload(self):
        """Tests if sending a valid mp4 file as a POST request to "/" responds with 302 status code."""

        with open(self.mp4, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

        try:
            self.assertEqual(res.status_code, 302)
            self.assertTrue(res.url.startswith('/watch'))

        except Exception as err:
            raise err
        
        finally:
            # Delete uploaded file
            # Get param that comes after "v="

            video_id = extract_id(res.url)    
            Video.objects.get(id=video_id).delete()


    def test_no_file(self):
        """Tests if omitting the file parameter from the POST request to "/" responds with a 400 status code."""

        res = self.client.post('/', {'title': 'Hello'})
        self.assertEqual(res.status_code, 400)


    def test_empty_file(self):
        """Tests if sending a video file of size 0 bytes as a POST request to "/" responds with a 400 status code."""

        with open(self.empty, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

            self.assertEqual(res.status_code, 400)
            self.assertTemplateUsed(res, 'error.html')


    def test_non_video_file(self):
        """Tests if sending a non-video file as a POST request to "/" responds with a 400 status code."""

        with open(self.non_video, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

            self.assertEqual(res.status_code, 400)
            self.assertTemplateUsed(res, 'error.html')


    def test_upload_time_limit(self):
        """Tests if sending a video that is over 60s in duration as a POST request to "/" responds with a 400 status code."""

        with open(self.time_limit, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

            self.assertEqual(res.status_code, 400)
            self.assertTemplateUsed(res, 'error.html')


    def test_upload_size_limit(self):
        """Tests if sending a video that is over 50MB in size as a POST request to "/" responds with a 400 status code."""

        with open(self.size_limit, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': ''})

            self.assertEqual(res.status_code, 400)
            self.assertTemplateUsed(res, 'error.html')


    def test_over_max_title(self):
        """Tests if a title over 50 characters in length in the POST request to "/" responds with a 400 status code."""

        title = 51 * 'h'

        with open(self.webm, mode="rb") as file:
            res = self.client.post('/', {'file': file, 'title': title})

            self.assertEqual(res.status_code, 400)
            self.assertTemplateUsed(res, 'error.html')


class WatchPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Initializes unchanging variables over all tests."""

        BASE_DIR: Path = Path(__file__).resolve().parent / 'test_files'
        cls.video: Path = BASE_DIR / 'webm_video.webm'

        # Upload expired video, pause for 10 minutes for video to expire, then create unexpired video

        client = Client()
        with open(cls.video, mode="rb") as file:
            res = client.post('/', {'file': file, 'title': 'expired-test'})
        
        cls.expired_id = extract_id(res.url)

        # wait for 10 minutes for video to expire.

        time.sleep(600)

        # Upload regular video.

        with open(cls.video, mode="rb") as file:
            res = client.post('/', {'file': file, 'title': 'video-test'})

        cls.id = extract_id(res.url)


    def setUp(self):
        """Sets up file upload for every test run."""


    def test_no_id(self):
        """Tests if GET requesting "/watch?v=" with the "v" query parameter missing responds with status code 400."""

        res = self.client.get(f'/watch')

        self.assertEqual(res.status_code, 400, msg=f'Requesting "/watch" with no query parameter v, responded with status code {res.status_code}.')
        self.assertTemplateUsed(res, 'error.html')

        
    def test_invalid_video_id(self):
        """Tests if GET requesting "/watch?v=" with a non-existent value for v query parameter responds with status code 404."""

        id = get_random_string(length=6)
        res = self.client.get(f'/watch?v={id}')

        self.assertEqual(res.status_code, 404, msg=f'Requesting "/watch?v={id}" with non-existent value for v, responded with status code {res.status_code}.')
        self.assertTemplateUsed(res, 'error.html')


    def test_expired_video_id(self):
        """Tests if GET requesting "/watch?v=" when the video URL has expired responds with status code 403."""

        id = self.expired_id
        res = self.client.get(f'/watch?v={id}')

        try:
            self.assertEqual(res.status_code, 403, msg=f'Requesting the expired endpoint "/watch?v={id}" responded with status code {res.status_code}.')
            self.assertTemplateUsed(res, 'error.html')

        except Exception as err:
            raise err
        
        finally:
            # Delete uploaded video

            Video.objects.get(id=id).delete()


    def test_valid_video_id(self):
        """Tests if GET requesting "/watch?v=" with a valid value for v query parameter responds with status code 200."""

        id = self.id
        res = self.client.get(f'/watch?v={id}')

        self.assertEqual(res.status_code, 200, msg=f'Requesting "/watch?v={id}" with a valid value for v, responded with status code {res.status_code}.')
        self.assertTemplateUsed(res, 'watch.html')


    def test_view_count_updates(self):
        """Tests if the view count updates when a video is visited."""

        # video page is loaded, middleware is then executed which updates viewcount by 1
        
        id = self.id
        old_viewcount: int = Video.objects.get(id=id).views

        self.client.get(f'/watch?v={id}')

        new_viewcount: int = Video.objects.get(id=id).views

        try:
            self.assertGreater(new_viewcount, old_viewcount, msg=f'View count is not incremented when "/watch?v={id}" is visited.')

        except Exception as err:
            raise err
        
        finally:
            # Delete uploaded video

            Video.objects.get(id=id).delete()
