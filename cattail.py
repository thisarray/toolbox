"""Python 3 script to print lines containing trailing whitespace."""

if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        for i, line in enumerate(f, 1):
            cleaned = line.rstrip()
            if (cleaned + '\n') != line:
                print('Line {}: {}'.format(i, cleaned))
