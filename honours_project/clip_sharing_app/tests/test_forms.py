from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import UploadForm

class UploadFormTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Initializes unchanging variables."""

        cls.test_dir = 'test_files/'
        cls.ideal = 'webm_video.webm'


    def setUp(self):
        ...


    def test_title_over_max_length(self):
        """Test if form accepts titles over 50 characters long."""

        title = 51 * 'a'
        file = SimpleUploadedFile(self.test_dir + self.ideal, b'file_content', content_type='video/webm')

        form = UploadForm(data={'title': title}, files={'file': file})

        self.assertFalse(form.is_valid(), msg='Form accepts title that is 51 characters long.')


    def test_max_length_title(self):
        """Test if form accepts titles that are 50 characters long."""

        title = 50 * 'a'
        file = SimpleUploadedFile(self.test_dir + self.ideal, b'file_content', content_type='video/webm')

        form = UploadForm(data={'title': title}, files={'file': file})

        self.assertTrue(form.is_valid(), msg='Form does not accept title that is 50 characters long.')


    def test_empty_title(self):
        """Test if form accepts empty string as title."""

        title = ''
        file = SimpleUploadedFile(self.test_dir + self.ideal, b'file_content', content_type='video/webm')

        form = UploadForm(data={'title': title}, files={'file': file})

        self.assertTrue(form.is_valid(), msg='Form does not accept empty title.')