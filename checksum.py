"""Python 3 script to calculate the checksums of files."""

import hashlib
import os.path
import unittest

_DEFAULT_HASH = 'sha256'
"""String name of the default hash algorithm in hashlib to use."""

# Set this larger than 2047 bytes so the Python GIL is released
_SIZE = 2048
"""Positive integer number of bytes to read from a file at a time."""

def checksum(path, name=_DEFAULT_HASH, size=_SIZE):
    """Return the string hexadecimal digest checksum of the file at path.

    Args:
        path: String path to the file.
        name: Optional string name of the hash algorithm in hashlib to use.
            Defaults to _DEFAULT_HASH.
        size: Optional positive int number of bytes to read from the file at
            a time. Defaults to _SIZE.
    Returns:
        String hexadecimal digest checksum of the file at path.
    """
    if not isinstance(path, str):
        raise TypeError('path must be a valid string path to a file.')
    if not os.path.isfile(path):
        raise ValueError('path must be a valid string path to a file.')
    if not isinstance(name, str):
        raise TypeError('name must be a string.')
    if not isinstance(size, int):
        raise TypeError('size must be a positive int > 1024.')
    if size <= 1024:
        raise ValueError('size must be a positive int > 1024.')

    name = name.strip().lower()
    m = hashlib.new(name)
    with open(path, 'rb') as f:
        while True:
            # read() returns '' once EOF is reached and else breaks the loop
            data = f.read(size)
            if len(data) > 0:
                m.update(data)
            else:
                break
    return m.hexdigest()


class _UnitTest(unittest.TestCase):
    def test_checksum(self):
        """Test calculating the checksum for a file."""
        for value in [None, 42.0, []]:
            self.assertRaises(TypeError, checksum, value)
            self.assertRaises(TypeError, checksum, 'checksum.py', value)
            self.assertRaises(TypeError, checksum, 'checksum.py', size=value)
        for value in ['', 'foobar']:
            self.assertRaises(ValueError, checksum, value)
            self.assertRaises(ValueError, checksum, 'checksum.py', value)
            self.assertRaises(TypeError, checksum, 'checksum.py', size=value)
        for value in range(-1, 1025):
            self.assertRaises(ValueError, checksum, 'checksum.py', size=value)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', default=[],
                        help='paths to files to checksum')
    args = parser.parse_args()

    if len(args.paths) <= 0:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        hash_name = _DEFAULT_HASH
        paths = []
        for path in args.paths:
            if path in hashlib.algorithms_available:
                hash_name = path
            elif os.path.isfile(path):
                paths.append(path)
        paths.sort()
        for path in paths:
            print('{0}  {1}'.format(checksum(path, hash_name),
                                    os.path.basename(path)))
