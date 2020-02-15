"""Python 3 script to print the current UTC date and time."""

import datetime
import unittest

WHITE_LIST = 'AaBbcdfGHIjMmpSUuVWwXxYyZz%'
"""List of format codes Python understands."""

NEW_CODE_MAP = {
    'C': lambda dt: '{0:04d}'.format(dt.year)[:2],
    'D': lambda dt: '%m/%d/%y',
    'e': lambda dt: ' %d',
    'F': lambda dt: '%Y-%m-%d',
    'g': lambda dt: dt.strftime('%G')[-2:],
    'h': lambda dt: '%b',
    'k': lambda dt: ' %H',
    'l': lambda dt: ' %I',
    'N': lambda dt: '{0:09d}'.format(dt.microsecond * 1000),
    'n': lambda dt: '\n',
    'q': lambda dt: '{0:d}'.format(((dt.month - 1) // 3) + 1),
    'P': lambda dt: dt.strftime('%p').lower(),
    'R': lambda dt: '%H:%M',
    'r': lambda dt: '%I:%M:%S %p',
    's': lambda dt: str(dt.timestamp()),
    'T': lambda dt: '%H:%M:%S',
    't': lambda dt: '\t'
}
"""Dictionary mapping a format code to its replacement function."""

def format_datetime(dt, format_string):
    """Return a string containing dt formatted according to format_string.

    Args:
        dt: datetime.datetime to format.
        format_string: String format string to follow.
    Returns:
        String containing dt formatted according to format_string.
    """
    if not isinstance(dt, datetime.datetime):
        raise TypeError('dt must be a datetime.datetime.')
    if not isinstance(format_string, str):
        raise TypeError('format_string must be a string.')

    # Need to scan format_string for format code sequences
    # Cannot just use replace() due to tricky cases like "%%Y"
    previous_character = None
    end = 0
    parts = []
    for i, c in enumerate(format_string):
        if previous_character == '%':
            previous_character = None
            if c in WHITE_LIST:
                # The format code is one recognized by Python
                continue
            parts.append(format_string[end:i-1])
            end = i + 1
            if c in NEW_CODE_MAP:
                parts.append(NEW_CODE_MAP[c](dt))
        else:
            previous_character = c
    parts.append(format_string[end:])
    return dt.strftime(''.join(parts))

class _UnitTest(unittest.TestCase):
    def test_constants(self):
        """Test the module constants."""
        for key in WHITE_LIST:
            self.assertNotIn(key, NEW_CODE_MAP)
            if key != '%':
                self.assertTrue(key.isalpha())
        for key, value in NEW_CODE_MAP.items():
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 1)
            self.assertTrue(key.isalpha())
            self.assertNotIn(key, WHITE_LIST)
            self.assertTrue(callable(value))

    def test_format_datetime(self):
        """Test formatting a datetime according to a format string."""
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        for value in [None, 42, []]:
            self.assertRaises(TypeError, format_datetime, value, '')
            self.assertRaises(TypeError, format_datetime, utc_now, value)
        for value in WHITE_LIST[:-1]:
            self.assertEqual(format_datetime(utc_now, value), value)
            self.assertGreater(len(format_datetime(utc_now, '%' + value)), 0)
            self.assertEqual(format_datetime(utc_now, '%%' + value),
                             '%' + value)
        for value, expected in [
            ('', ''),
            ('%%', '%'),
            ('%Y', '{0:04d}'.format(utc_now.year)),
            ('%m', '{0:02d}'.format(utc_now.month)),
            ('%d', '{0:02d}'.format(utc_now.day)),
            ('%C', '20'),
            ('%D', utc_now.strftime('%m/%d/%y')),
            ('%e', utc_now.strftime(' %d')),
            ('%F', utc_now.strftime('%Y-%m-%d')),
            ('%g', utc_now.strftime('%G')[-2:]),
            ('%h', utc_now.strftime('%b')),
            ('%k', utc_now.strftime(' %H')),
            ('%l', utc_now.strftime(' %I')),
            ('%n', '\n'),
            ('%R', utc_now.strftime('%H:%M')),
            ('%r', utc_now.strftime('%I:%M:%S %p')),
            ('%T', utc_now.strftime('%H:%M:%S')),
            ('%t', '\t')]:
            self.assertEqual(format_datetime(utc_now, value), expected)
            for c in WHITE_LIST[:-1]:
                self.assertEqual(format_datetime(utc_now, c + value),
                                 c + expected)
                self.assertEqual(format_datetime(utc_now, value + c),
                                 expected + c)
                self.assertEqual(format_datetime(utc_now, c + value + c),
                                 c + expected + c)
        if utc_now.hour < 12:
            self.assertEqual(format_datetime(utc_now, '%P'), 'am')
            self.assertEqual(format_datetime(utc_now, '%p'), 'AM')
        else:
            self.assertEqual(format_datetime(utc_now, '%P'), 'pm')
            self.assertEqual(format_datetime(utc_now, '%p'), 'PM')
        for value in range(1, 13):
            utc_now = utc_now.replace(month=value)
            if value < 4:
                expected = '1'
            elif value < 7:
                expected = '2'
            elif value < 10:
                expected = '3'
            else:
                expected = '4'
            self.assertEqual(format_datetime(utc_now, '%q'), expected)
            utc_now = utc_now.replace(microsecond=0, tzinfo=None)
            self.assertEqual(format_datetime(utc_now, '%Y-%m-%dT%H:%M:%S'),
                             utc_now.isoformat())
            self.assertEqual(format_datetime(utc_now, '%Y-%m-%d %H:%M:%S'),
                             utc_now.isoformat(sep=' '))

        dt = datetime.datetime(2001, 2, 3, 4, 5, 6, 7)
        for value, expected in [
            ('', ''),
            ('%%', '%'),
            ('%A', 'Saturday'),
            ('%a', 'Sat'),
            ('%B', 'February'),
            ('%b', 'Feb'),
            ('%C', '20'),
            ('%c', 'Sat Feb  3 04:05:06 2001'),
            ('%D', '02/03/01'),
            ('%d', '03'),
            ('%e', ' 03'),
            ('%F', '2001-02-03'),
            ('%G', '2001'),
            ('%g', '01'),
            ('%H', '04'),
            ('%h', 'Feb'),
            ('%I', '04'),
            ('%j', '034'),
            ('%k', ' 04'),
            ('%l', ' 04'),
            ('%M', '05'),
            ('%m', '02'),
            ('%N', '000007000'),
            ('%n', '\n'),
            ('%P', 'am'),
            ('%p', 'AM'),
            ('%q', '1'),
            ('%R', '04:05'),
            ('%r', '04:05:06 AM'),
            ('%S', '06'),
            ('%s', '981201906.000007'),
            ('%T', '04:05:06'),
            ('%t', '\t'),
            ('%U', '04'),
            ('%u', '6'),
            ('%V', '05'),
            ('%W', '05'),
            ('%w', '6'),
            ('%X', '04:05:06'),
            ('%x', '02/03/01'),
            ('%Y', '2001'),
            ('%y', '01'),
            ('Today is %A, %B %d, %Y',
             'Today is Saturday, February 03, 2001'),
            ('Today is %A, %B%e, %Y',
             'Today is Saturday, February 03, 2001'),
            ('The current time is %H:%M:%S %p',
             'The current time is 04:05:06 AM')]:
            self.assertEqual(format_datetime(dt, value), expected)
            for c in WHITE_LIST[:-1]:
                self.assertEqual(format_datetime(dt, c + value),
                                 c + expected)
                self.assertEqual(format_datetime(dt, value + c),
                                 expected + c)
                self.assertEqual(format_datetime(dt, c + value + c),
                                 c + expected + c)

        dt = datetime.datetime(2011, 12, 13, 14, 15, 16, 17)
        for value, expected in [
            ('', ''),
            ('%%', '%'),
            ('%A', 'Tuesday'),
            ('%a', 'Tue'),
            ('%B', 'December'),
            ('%b', 'Dec'),
            ('%C', '20'),
            ('%c', 'Tue Dec 13 14:15:16 2011'),
            ('%D', '12/13/11'),
            ('%d', '13'),
            ('%e', ' 13'),
            ('%F', '2011-12-13'),
            ('%G', '2011'),
            ('%g', '11'),
            ('%H', '14'),
            ('%h', 'Dec'),
            ('%I', '02'),
            ('%j', '347'),
            ('%k', ' 14'),
            ('%l', ' 02'),
            ('%M', '15'),
            ('%m', '12'),
            ('%N', '000017000'),
            ('%n', '\n'),
            ('%P', 'pm'),
            ('%p', 'PM'),
            ('%q', '4'),
            ('%R', '14:15'),
            ('%r', '02:15:16 PM'),
            ('%S', '16'),
            ('%s', '1323814516.000017'),
            ('%T', '14:15:16'),
            ('%t', '\t'),
            ('%U', '50'),
            ('%u', '2'),
            ('%V', '50'),
            ('%W', '50'),
            ('%w', '2'),
            ('%X', '14:15:16'),
            ('%x', '12/13/11'),
            ('%Y', '2011'),
            ('%y', '11'),
            ('Today is %A, %B %d, %Y',
             'Today is Tuesday, December 13, 2011'),
            ('Today is %A, %B%e, %Y',
             'Today is Tuesday, December 13, 2011'),
            ('The current time is %H:%M:%S %p',
             'The current time is 14:15:16 PM')]:
            self.assertEqual(format_datetime(dt, value), expected)
            for c in WHITE_LIST[:-1]:
                self.assertEqual(format_datetime(dt, c + value),
                                 c + expected)
                self.assertEqual(format_datetime(dt, value + c),
                                 expected + c)
                self.assertEqual(format_datetime(dt, c + value + c),
                                 c + expected + c)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--test', action='store_true',
                        help='run the unit tests')
    parser.add_argument('-I', '--iso-8601', action='store_true',
                        help='output in ISO 8601 format')
    parser.add_argument('-R', '--rfc-2822', action='store_true',
                        help='output in RFC 2822 format')
    parser.add_argument('--rfc-3339', action='store_true',
                        help='output in RFC 3339 format')
    parser.add_argument('format', nargs='?', default='',
                        help='format string to follow')
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
        parser.exit()

    format_string = '%Y-%m-%dT%H:%M:%S%z'
    if args.iso_8601:
        # Default to ISO 8601 format
        pass
    elif args.rfc_2822:
        format_string = '%a, %d %b %Y %H:%M:%S %z'
    elif args.rfc_3339:
        format_string = '%Y-%m-%d %H:%M:%S%z'
    elif len(args.format) > 0:
        format_string = args.format
    print(format_datetime(datetime.datetime.now(datetime.timezone.utc),
                          format_string))
