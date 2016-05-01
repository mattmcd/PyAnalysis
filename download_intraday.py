import argparse
from mda.finance import get_all

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download intraday FTSE100 data')
    parser.add_argument('--do-copy', dest='do_copy', action='store_true',
                        help='Copy files to S3')
    args = parser.parse_args()
    get_all(do_copy=args.do_copy)

