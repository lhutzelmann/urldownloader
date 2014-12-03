# coding=utf-8

import codecs
import argparse
import string
import urllib2
import sys

class UrlDownloader(object):
    """ Class to download a file from a given URL.
    """
    def __extract_filename(self, text_url):
        """
        :param text_url: URL as text string
        :return: the file name extracted from the URL
        """
        return text_url.split('?')[0].rsplit('/', 1)[1]

    def download(self, text_url):
        """
        :param text_url: URL as text string
        """
        print u'Downloading %s' % text_url

        response = urllib2.urlopen(text_url)
        stat = response.getcode()

        if stat == 200:
            filename = self.__extract_filename(text_url)
            with open(filename, 'wb') as f:
                f.write(response.read())
        else:
            raise RuntimeError("Response status = %d" % stat)

def main(encoding='utf-8'):
    # Set up argument parser.
    parser = argparse.ArgumentParser(
        description='Download web content from text URLs in a file.')
    parser.add_argument('file', metavar='FILE', nargs='+',
                        help='a file which contains one URL per line')
    parser.add_argument('-e', '--encoding', default=encoding,
                        help=('set the encoding of the file (default=%s)' %
                              encoding))

    args = parser.parse_args()

    url_downloader = UrlDownloader()

    exit_code = None
    for file_path in args.file:
        with codecs.open(file_path, encoding=args.encoding) as f:
            for url in f:
                url = string.strip(url)   # remove whitespace
                try:
                    url_downloader.download(url)
                except Exception as e:
                    print "Error occurred: %s" % e
                    exit_code = 1
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
