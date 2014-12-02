# coding=utf-8

import codecs
import argparse

def download_url(text_url):
    print u'Downloading %s' % text_url
    # ToDo: check validity of text_url
    # ToDo: do the download

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

    for file_path in args.file:
        with codecs.open(file_path, encoding=args.encoding) as f:
            for url in f:
                download_url(url)

if __name__ == '__main__':
    main()
