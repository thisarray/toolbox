"""Python 3 script to get an URL."""

import urllib.parse
import unittest

def is_valid_url(url, minimum_length=4):
    """Return whether url is a valid URL string.

    Args:
        url: String URL to test.
        minimum_length: Optional integer minimum length for the URL parts.
            Defaults to 4 because URL needs at least a scheme like "http"
            and a domain like ".com".
    Returns:
        True if url is a valid URL string. False otherwise.
    """
    if not isinstance(minimum_length, int):
        raise TypeError('minimum_length must be a positive int.')
    if minimum_length < 1:
        raise ValueError('minimum_length must be a positive int.')

    if not isinstance(url, str):
        return False
    if len(url) < minimum_length:
        return False
    parts = urllib.parse.urlparse(url)
    if len(parts.scheme) < minimum_length:
        return False
    if len(parts.netloc) < minimum_length:
        return False
    return True

class _UnitTest(unittest.TestCase):
    def test_is_valid_url(self):
        """Test if an URL is valid."""
        for value in [None, '', [], 'foobar',
                      'http', 'https', 'http://', 'https://',
                      'example.com', '//example.com', 'ftp://example.com',
                      '//www.cwi.nl:80/%7Eguido/Python.html',
                      'www.cwi.nl/%7Eguido/Python.html', 'help/Python.html']:
            self.assertRaises(TypeError, is_valid_url,
                              'http://www.example.com', value)
            self.assertFalse(is_valid_url(value))
        for value in range(-1, 1):
            self.assertRaises(ValueError, is_valid_url,
                              'http://www.example.com', value)
        for value in ['http://example.com', 'https://example.com',
                      'file://example.com',
                      'http://www.example.com', 'https://www.example.com',
                      'file://www.example.com',
                      'http://www.cwi.nl:80/%7Eguido/Python.html']:
            self.assertTrue(is_valid_url(value))
            self.assertTrue(is_valid_url(value, 2))
            if value.startswith('https'):
                self.assertTrue(is_valid_url(value, 5))
                self.assertFalse(is_valid_url('http' + value[5:], 5))
            else:
                self.assertFalse(is_valid_url(value, 5))
                self.assertTrue(is_valid_url('https' + value[4:], 5))

if __name__ == '__main__':
    import argparse
    import os.path
    import urllib.request
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--output', default='',
                        help='write the response to the file at path')
    parser.add_argument('url',
                        help='URL to get')
    args = parser.parse_args()

    if os.path.exists(args.output):
        parser.error('{0} already exists!'.format(args.output))

    if is_valid_url(args.url):
        request = urllib.request.Request(args.url)
        with urllib.request.urlopen(request) as response:
            if len(args.output) <= 0:
                print(response.read().decode('utf-8'), end='')
            else:
                with open(args.output, 'wb') as f:
                    f.write(response.read())
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
