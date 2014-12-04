# coding=utf-8
# for testing with PyCharm uncheck "Add source roots to PYTHONPATH"
import unittest
from urldownloader.urldownloader import UrlDownloader
import mock
import tempfile
import os
import shutil
import codecs


def create_fake_response(code=200, message='MESSAGE'):
    """ Creates a mock response object.

    :param code: http status code
    :param message: payload data
    :return: the response object
    """
    mock_response = mock.Mock()
    mock_response.getcode.return_value = code
    mock_response.read.return_value = message
    return mock_response


class TestSuiteExtractFilename(unittest.TestCase):
    """ Test extraction of filename from URL.
    """

    def setUp(self):
        self.url_downloader = UrlDownloader()

    def test_extract_filename_ok(self):
        filename = self.url_downloader._extract_filename(
            'http://server/path/filename.jpg'
        )
        self.assertEqual('filename.jpg', filename)

    def test_extract_filename_unicode_ok(self):
        filename = self.url_downloader._extract_filename(
            u'http://server/path/filenäme.jpg'
        )
        self.assertEqual(u'filenäme.jpg', filename)

    def test_extract_filename_query(self):
        filename = self.url_downloader._extract_filename(
            'http://server/path/filename.jpg?arg=1'
        )
        self.assertEqual('filename.jpg', filename)

    def test_extract_filename_incompatible_scheme(self):
        """ URL schemes that have no path with '/' are not supported.
        """
        self.assertRaises(BaseException,
                          self.url_downloader._extract_filename,
                          'mailto:hans@example.org')

    def test_extract_filename_empty(self):
        """ Empty URLs are not supported.
        """
        self.assertRaises(BaseException,
                          self.url_downloader._extract_filename,
                          '')


class TestSuiteDownload(unittest.TestCase):
    """ Test download functionality.
    """

    def setUp(self):
        self.url_downloader = UrlDownloader()
        # prepare temporary dir for storing downloaded files
        self._old_cwd = os.getcwd()
        self._temp_dir = tempfile.mkdtemp()
        os.chdir(self._temp_dir)

    def tearDown(self):
        # clean up temporary dir
        os.chdir(self._old_cwd)
        shutil.rmtree(self._temp_dir)

    def validate_file_content(self, file_name, expected_content):
        file_content = (
            codecs.open(file_name, 'rb', encoding='utf-8')
            .read()
        )
        self.assertEqual(expected_content, file_content)

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download(self, mock_urllib2):
        """ Test download that succeeds.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.return_value = create_fake_response(200,
                                                                 'MESSAGE')

        self.url_downloader.download('http://server/path/filename.txt')

        self.validate_file_content('filename.txt', 'MESSAGE')

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download_server_failing(self, mock_urllib2):
        """ Test download that fails server side.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.return_value = create_fake_response(500,
                                                                 'MESSAGE')

        self.assertRaises(RuntimeError,
                          self.url_downloader.download,
                          'http://server/path/filename.txt')

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download_exception(self, mock_urllib2):
        """ Test download that fails due to some error when opening URL.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.side_effect = ValueError('Test error')

        self.assertRaises(ValueError,
                          self.url_downloader.download,
                          'http://server/path/filename.txt')

    # ToDo: unit tests for main(). Alternatively test it on system level.

if __name__ == '__main__':
    unittest.main()
