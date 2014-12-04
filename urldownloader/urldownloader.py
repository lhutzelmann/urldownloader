# coding=utf-8

import codecs
import argparse
import string
import urllib2
import sys

DEFAULT_ENCODING = 'utf-8'


class UrlDownloader(object):
    """ Class to download a file from a given URL.
    """
    # Implemented as class for better extensibility.
    # TODO: forbid non http-URLs

    def _extract_filename(self, text_url):
        """ Extracts the file name from the url.
        Requires the URL to contain the file name as last segment.
        Therefore no query parameters are allowed.

        :param text_url: URL as text string
        :return: the file name extracted from the URL
        """
        return text_url.split('?')[0].rsplit('/', 1)[1]

    def download(self, text_url):
        """ Perform the download. Opens the URL, retrieves the response data
        and saves it to a file using a file name extracted from the URL.
        The file is saved to the current working directory.

        :param text_url: URL as text string
        """
        print u'Downloading %s' % text_url

        response = urllib2.urlopen(text_url)
        stat = response.getcode()

        if stat == 200:
            filename = self._extract_filename(text_url)
            with open(filename, 'wb') as f:
                f.write(response.read())
        else:
            raise RuntimeError("Response status = %d" % stat)


def main(files, encoding=DEFAULT_ENCODING):
    """ Main function of the script. Performs the actual work and can be called
    from other code directly.

    :param files: Sequence of file paths to the files that contain the URLs.
    :param encoding: Defines the encoding of the input files.
    :return: True if everything went fine, False otherwise.
    """
    url_downloader = UrlDownloader()

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
    exit_code = None if no_error_occurred else 1
    sys.exit(exit_code)
