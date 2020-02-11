"""Python 3 script to get an URL."""

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

    request = urllib.request.Request(args.url)
    with urllib.request.urlopen(request) as response:
        if len(args.output) <= 0:
            print(response.read().decode('utf-8'))
        else:
            with open(args.output, 'wb') as f:
                f.write(response.read())
