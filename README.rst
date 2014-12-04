URL Downloader
==============

.. note:: This is a temporary example project for educational purposes.

Given a plaintext file containing URLs, one per line, e.g.::

    http://mywebserver.com/images/271947.jpg
    http://mywebserver.com/images/24174.jpg
    http://somewebsrv.com/img/992147.jpg

URL Downloader takes this plaintext file as an argument and downloads all images, storing them on the local hard disk.

Installation
------------

The software is not packaged at all, so no installation.

Usage
-----

.. note:: The script requires Python 2.7+ to run.

Type the following to see all options::

    python urldownloader/urldownloader.py -h

The `tests` folder contains a file with example URLs (pointing to some freely downloadable images plus an intentionally erroneous entry).

You can download them using the following command::

    python urldownloader/urldownloader.py tests/url_file.txt

Run tests
---------

.. note:: The tests require mock 1.0.1 for http-server mocking

You can run the tests as follows::

    cd <project dir>
    python -m unittest test_urldownloader

If you get the following, misleading error, you may need to install mock::

    AttributeError: 'module' object has no attribute 'test_urldownloader'


Suggestions for improvement
---------------------------

- an option to set a target folder
- support parallel downloading
- more automated tests (e.g. using mocking or a local http-server)
- support URLs that do not end with the file name
- handling of already existing files and/or duplicated names (but different content)
- proper packaging
