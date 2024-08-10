"""Sort the checksums found in the file at path case insensitively."""

if __name__ == '__main__':
    import argparse
    import os.path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'path', nargs='?', default='',
        help='path to the checksum file')
    args = parser.parse_args()

    if os.path.isfile(args.path):
        buffer = []
        with open(args.path, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned = line.strip()
                if len(cleaned) <= 0:
                    continue
                fields = cleaned.split(maxsplit=1)
                if len(fields) < 2:
                    continue
                if fields[1].startswith('*'):
                    # Remove asterisk in the checksum file
                    filename = fields[1].lstrip('*')
                else:
                    filename = fields[1]
                buffer.append((filename.lower(), filename, fields[0]))
        buffer.sort()
        for lowered, filename, checksum in buffer:
            print('{}  {}'.format(checksum, filename))
