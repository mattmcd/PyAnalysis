import argparse
from mda.finance import get_all, update_local, get_download_dates
from mda.io.google_finance import read_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FTSE100 data retrieval and analysis')
    parser.add_argument('action', help='Action: update, retrieve, dates, movers', action='store', default='update')
    parser.add_argument('-d', '--date', help='Data date', action='store', default=None)
    parser.add_argument('-n', '--number', help='Number of stocks to retrieve in top N', action='store', default=10)
    args = parser.parse_args()
    action = args.action
    if action == 'update':
        update_local()
    elif action == 'retrieve':
        get_all(do_copy=args.do_copy)
    elif action == 'dates':
        # List download dates
        print('Local dates:')
        dates = get_download_dates()
        print(' '.join(sorted(dates)))
    elif action == 'movers':
        if args.date is None:
            dates = get_download_dates()
            date = sorted(dates)[-1]
        else:
            date = args.date
        n = int(args.number)
        print('Reading data from ' + date)
        df = read_dir(date)
        df['day'] = df['date'].dt.strftime('%Y%m%d')
        df.set_index(['day', 'period', 'ticker'], inplace=True)
        df_close = df.unstack()['close'].ffill().dropna()
        df_close = df_close.div(df_close.iloc[0, :])
        print('Risers')
        print(df_close.iloc[-1, :].sort_values(ascending=False)[:n])
        print('Fallers')
        print(df_close.iloc[-1, :].sort_values(ascending=True)[:n])