import argparse
from mda.finance import get_all, update_local

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FTSE100 data retrieval and analysis')
    parser.add_argument('action', help='Action: update, retrieve', action='store', default='update')
    args = parser.parse_args()
    action = args.action
    if action == 'update':
        update_local()
    elif action == 'retrieve':
        get_all(do_copy=args.do_copy)
