"""Fold the lines found in the text file at path."""

if __name__ == '__main__':
    import argparse
    import os.path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-d', '--delimiter', default=', ',
        help='string delimiter separating the elements on a line (defaults to comma)')
    parser.add_argument(
        '-s', '--start', default='  ',
        help='string preceding the elements on a line (defaults to 2 spaces)')
    parser.add_argument(
        '-e', '--end', default=',',
        help='string following the elements on a line (defaults to comma)')
    parser.add_argument(
        '-w', '--width', type=int, default=10,
        help='integer number of elements per line')
    parser.add_argument(
        'path', nargs='?', default='',
        help='path to the text file to fold')
    args = parser.parse_args()

    if os.path.isfile(args.path):
        lines = []
        with open(args.path, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.strip())
        for i in range(0, len(lines), args.width):
            line = args.start + args.delimiter.join(lines[i:i+args.width]) + args.end
            print(line)
