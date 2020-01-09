"""Python 3 script to print the contents of files to standard output."""

if __name__ == '__main__':
    import argparse
    import os.path
    import textwrap
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-w', '--width', type=int, default=72,
                        help='integer width of the output lines')
    parser.add_argument('paths', nargs='*', default=[],
                        help='paths to files to print')
    args = parser.parse_args()

    wrapper = textwrap.TextWrapper(width=args.width)
    for path in args.paths:
        if os.path.isfile(path):
            with open(path, 'r') as f:
                for line in f:
                    cleaned = line.rstrip()
                    if len(cleaned) <= 0:
                        print()
                    else:
                        for output in wrapper.wrap(cleaned):
                            print(output)
