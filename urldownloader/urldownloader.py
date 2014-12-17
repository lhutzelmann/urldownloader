# coding=utf-8

import codecs
import contextlib
import argparse
import string
import urllib2
import sys

DEFAULT_ENCODING = 'utf-8'


def http_url_filename_extract(http_url):
    """ Extracts the file name from the url.
    Requires the URL to contain the file name as last segment.
    Therefore no query parameters are allowed.

    :param http_url: URL as text string
    :return: the file name extracted from the URL
    """
    return http_url.split('?')[0].rsplit('/', 1)[1]


@contextlib.contextmanager  # adds 'with' context support
def http_download(text_url):
    """ Perform the download. Opens the URL and returns a stream object.
    The returned stream must either be closed or used in a 'with' context.

    :param text_url: URL as text string
    :return: stream to payload data
    """
    response = urllib2.urlopen(text_url)
    stat = response.getcode()
    if stat != 200:
        raise RuntimeError("Response status = %d" % stat)

    yield response
    response.close()


class UrlDownloader(object):
    """ Class to download a file from a given URL.
    """

    def __init__(self, filename_extractor, downloader):
        """ Initialize the URL downloader of a given type
        :param filename_extractor: callable file name extractor returning a
                                   file name from the given URL
        :param downloader: callable downloader returning a data stream from the
                           given URL
        """
        self._filename_extractor = filename_extractor
        self._downloader = downloader

    def download(self, text_url):
        """ Perform the download. Opens the URL, retrieves the data
        and saves it to a file using a file name extracted from the URL.
        The file is saved to the current working directory.

        :param text_url: URL as text string
        """
        print u'Downloading %s' % text_url

        filename = self._filename_extractor(text_url)
        with self._downloader(text_url) as source_stream:
            with open(filename, 'wb') as target_stream:
                target_stream.write(source_stream.read())


def main(files, encoding=DEFAULT_ENCODING):
    """ Main function of the script. Performs the actual work and can be called
    from other code directly.

    :param files: Sequence of file paths to the files that contain the URLs.
    :param encoding: Defines the encoding of the input files.
    :return: True if everything went fine, False otherwise.
    """
    # TODO: Add more downloaders for future supported protocols
    # Currently only http supported.
    url_downloader = UrlDownloader(
        http_url_filename_extract,
        http_download
    )

    no_error = True
    for file_path in files:
        with codecs.open(file_path, encoding=encoding) as f:
            for url in f:
                url = string.strip(url)   # remove whitespace
                try:
                    url_downloader.download(url)
                except Exception as e:
                    print "Error occurred: %s" % e
                    no_error = False
    return no_error

if __name__ == '__main__':
    # Set up argument parser for command line handling.
    parser = argparse.ArgumentParser(
        description='Download web content from URLs in files.')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='file which contains one URL per line')
    parser.add_argument('-e', '--encoding', default=DEFAULT_ENCODING,
                        help=('set the encoding of the file(s) (default=%s)' %
                              DEFAULT_ENCODING))

    # Get command line arguments as a dictionary.
    kwargs = vars(parser.parse_args())

    no_error_occurred = main(**kwargs)

    # set exit code depending on an occurred error
    exit_code = None if no_error_occurred else 1
    sys.exit(exit_code)
