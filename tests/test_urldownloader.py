# coding=utf-8
# for testing with PyCharm uncheck "Add source roots to PYTHONPATH"
import contextlib
import unittest
import urldownloader.urldownloader as udl
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
        self._filename_extractor = udl.http_url_filename_extract

    def test_extract_filename_ok(self):
        filename = self._filename_extractor(
            'http://server/path/filename.jpg'
        )
        self.assertEqual('filename.jpg', filename)

    def test_extract_filename_unicode_ok(self):
        filename = self._filename_extractor(
            u'http://server/path/filenäme.jpg'
        )
        self.assertEqual(u'filenäme.jpg', filename)

    def test_extract_filename_query(self):
        filename = self._filename_extractor(
            'http://server/path/filename.jpg?arg=1'
        )
        self.assertEqual('filename.jpg', filename)

    def test_extract_filename_incompatible_scheme(self):
        """ URL schemes that have no path with '/' are not supported.
        """
        self.assertRaises(BaseException,
                          self._filename_extractor,
                          'mailto:hans@example.org')

    def test_extract_filename_empty(self):
        """ Empty URLs are not supported.
        """
        self.assertRaises(BaseException,
                          self._filename_extractor,
                          '')


class TestSuiteHttpDownload(unittest.TestCase):
    """ Test HTTP download functionality.
    """
    def setUp(self):
        self._downloader = udl.http_download

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download(self, mock_urllib2):
        """ Test download that succeeds.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.return_value = create_fake_response(200,
                                                                 'MESSAGE')

        with self._downloader('http://server/path/filename.txt') as stream:
            data = stream.read()
        self.assertEqual('MESSAGE', data)

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download_server_failing(self, mock_urllib2):
        """ Test download that fails server side.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.return_value = create_fake_response(500,
                                                                 'MESSAGE')
        with self.assertRaises(RuntimeError):
            with self._downloader('http://server/path/filename.txt') as stream:
                data = stream.read()

    @mock.patch('urldownloader.urldownloader.urllib2')
    def test_download_exception(self, mock_urllib2):
        """ Test download that fails due to some error when opening URL.
        """
        # set mock result for urlopen
        mock_urllib2.urlopen.side_effect = ValueError('Test error')

        with self.assertRaises(ValueError):
            with self._downloader('http://server/path/filename.txt') as stream:
                data = stream.read()


class TestSuiteUrlDownloader(unittest.TestCase):
    """ Test UrlDownloader class functionality.
    """

    def setUp(self):
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

    def get_filename_extractor(self, filename):
        # TODO: can mock be used instead?
        def func(text_url):
            return filename
        return func

    def get_downloader(self, code=200, message='MESSAGE'):
        # TODO: can mock be used instead?
        @contextlib.contextmanager
        def func(text_url):
            yield create_fake_response(code, message)
        return func

    def test_download(self):
        """ Test download that succeeds.
        """
        url_downloader = udl.UrlDownloader(
            self.get_filename_extractor('filename.txt'),
            self.get_downloader(200, 'MESSAGE')
        )

        url_downloader.download('http://server/path/filename.txt')

        self.validate_file_content('filename.txt', 'MESSAGE')

    def test_download_server_failing(self):
        """ Test download that fails server side.
        """
        mock_callable = mock.Mock()
        mock_callable.side_effect = RuntimeError('Test error')
        url_downloader = udl.UrlDownloader(
            self.get_filename_extractor('filename.txt'),
            mock_callable
        )

        self.assertRaises(RuntimeError,
                          url_downloader.download,
                          'http://server/path/filename.txt')

    def test_download_exception(self):
        """ Test download that fails due to some error when opening URL.
        """
        mock_callable = mock.Mock()
        mock_callable.side_effect = ValueError('Test error')
        url_downloader = udl.UrlDownloader(
            self.get_filename_extractor('filename.txt'),
            mock_callable
        )
        self.assertRaises(ValueError,
                          url_downloader.download,
                          'http://server/path/filename.txt')

    def test_filename_extractor_exception(self):
        """ Test download that fails due to some error when opening URL.
        """
        mock_callable = mock.Mock()
        mock_callable.side_effect = ValueError('Test error')
        url_downloader = udl.UrlDownloader(
            mock_callable,
            self.get_downloader(200, 'MESSAGE')
        )
        self.assertRaises(ValueError,
                          url_downloader.download,
                          'http://server/path/filename.txt')

    # ToDo: unit tests for main(). Alternatively test it on system level.

if __name__ == '__main__':
    unittest.main()
