"""Python 3 script to simulate die rolls using the secrets module."""

import string

# string.hexdigits repeats abcdef
HEX_DIGITS = string.digits + 'ABCDEF'
"""String characters in a hex digit."""

if __name__ == '__main__':
    import argparse
    import secrets
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c', '--characters', default='',
        help='add the specified characters to the alphabet')
    parser.add_argument(
        '-d', '--digits', action='store_true',
        help='add ' + string.digits + ' to the alphabet')
    parser.add_argument(
        '-l', '--lower', action='store_true',
        help='add ' + string.ascii_lowercase + ' to the alphabet')
    parser.add_argument(
        '-o', '--octal', action='store_true',
        help='add ' + string.octdigits + ' to the alphabet')
    parser.add_argument(
        '-p', '--punctuation', action='store_true',
        help='add punctuation characters to the alphabet')
    parser.add_argument(
        '-u', '--upper', action='store_true',
        help='add ' + string.ascii_uppercase + ' to the alphabet')
    parser.add_argument(
        '-x', '--hex', action='store_true',
        help='add ' + HEX_DIGITS + ' to the alphabet')
    parser.add_argument(
        'count', type=int, default=16,
        help='integer number of die rolls (length of output)')
    args = parser.parse_args()

    alphabet = set()
    if len(args.characters) > 0:
        alphabet.update(args.characters)
    if args.digits:
        alphabet.update(string.digits)
    if args.lower:
        alphabet.update(string.ascii_lowercase)
    if args.octal:
        alphabet.update(string.octdigits)
    if args.punctuation:
        alphabet.update(string.punctuation)
    if args.upper:
        alphabet.update(string.ascii_uppercase)
    if args.hex:
        alphabet.update(HEX_DIGITS)

    if len(alphabet) > 0:
        alphabet = ''.join(sorted(alphabet))
        print('Using alphabet "{}"'.format(alphabet))
        print(''.join(secrets.choice(alphabet) for i in range(args.count)))
