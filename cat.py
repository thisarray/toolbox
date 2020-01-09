"""Python 3 script to print the contents of files to standard output."""

if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        for line in f:
            print(line.rstrip())
