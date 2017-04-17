import mda
import urllib2
import numpy as np
import pandas as pd
import os

ftseFile = mda.data_dir('FTSE100', 'FTSE100.csv')


class LseReader:
    def __init__(self, interval=60, period=10):
        """Constructor
        :param interval: time in seconds between downloaded values
        :param period: period in days to download
        :return: LseReader
        """

        self.ftse100 = pd.read_csv(ftseFile)
        self.prefixURL = 'https://www.google.com/finance/getprices?'
        self.interval = interval
        self.period = period

    def read_url(self, ticker, interval=None, period=None):
        """Read intraday history for selected ticker on LSE
        :param interval: time in seconds between downloaded values
        :param period: period in days to download
        :return: txt : downloaded price data as string
        :return: interval : interval in seconds between downloaded prices
        """
        if not interval:
            interval = self.interval
        if not period:
            period = self.period

        txt = urllib2.urlopen(
            (self.prefixURL + 'q={Ticker}&x=LON&i={Interval}' +
             '&p={Period}d&f=d,o,h,l,c,v').format(
                Ticker=ticker, Interval=interval, Period=period)).read()
        return txt, interval

    def read_history(self, ticker, interval=None, period=None):
        """Read intraday history for selected ticker on LSE
        :param interval: time in seconds between downloaded values
        :param period: period in days to download
        :return: df : downloaded price data as pandas DataFrame
        """
        txt, interval = self.read_url(ticker, interval, period)
        df = parse_text(txt, ticker=ticker)
        return df


def parse_ohlc(cols, interval, recs, ticker):
    df = pd.DataFrame(recs, columns=cols)
    for col in cols[1:]:
        df[col] = pd.to_numeric(df[col])
    dates = np.zeros(df.date.shape, dtype=pd.Timestamp)
    period = np.zeros(df.date.shape, dtype=int)
    last_date = pd.Timestamp(0)
    for i, date_str in enumerate(df.date):
        if not date_str:
            continue
        if date_str[0].lower() == 'a':
            last_date = pd.to_datetime(int(date_str[1:]), unit='s')
            dates[i] = last_date
            period[i] = 0
        else:
            # Offset
            try:
                this_date = last_date + pd.to_timedelta(int(date_str) * interval, unit='s')
                dates[i] = this_date
                period[i] = int(date_str)
            except ValueError as ex:
                print(ticker + ': ' + ex.message)
    df['date'] = dates
    df['period'] = period
    if ticker:
        df['ticker'] = ticker
    return df


def parse_text(txt, ticker=None):
    lines = txt.split('\n')
    # Find line where data starts
    data_ind = next(i for i, el in enumerate(lines) if 'DATA=' in el)
    # Find lines where the timezone offset is specified.  If there has been no
    # change in timezone there will only be one, immediately after the
    # DATA= line, however when the clocks change (BST) there will be two
    tz_lines = [i for i, el in enumerate(lines) if 'TIMEZONE_OFFSET=' in el]
    if len(tz_lines) == 0:
        return None
    tz_lines.append(-1)
    # Extract the header key value pairs.  We ignore the first line of the file
    # which indicates the exchange.
    header = {k.lower(): v.lower() for (k, v) in
              [tuple(line.split('=')) for line in lines[1:data_ind]]}
    header['columns'] = header['columns'].split(',')
    for field in ['interval', 'market_close_minute', 'market_open_minute']:
        header[field] = int(header[field])
    # Extract the price data, appending column for the timezone offset
    res = []
    for i in range(0, len(tz_lines)-1):
        tz_offset = int(lines[tz_lines[i]].split('=')[1])
        recs = [dict(zip(header['columns'], line.split(',')))
                for line in lines[tz_lines[i]+1:tz_lines[i+1]]]
        df = parse_ohlc(header['columns'], header['interval'], recs, ticker=ticker)
        df['tz_offset'] = tz_offset
        res.append(df)
    df = pd.concat(res).reset_index(drop=True)
    return df


def read_file(ticker_file, datestr):
    with open(mda.data_dir('FTSE100', datestr, ticker_file)) as f:
        return parse_text(f.read(), ticker=ticker_file.split('.')[0])


def read_dir(datestr, print_date=False):
    if print_date:
        print(datestr)
    return pd.concat(
        [read_file(f, datestr)
         for f in os.listdir(mda.data_dir('FTSE100', datestr))])


def read_dates(dates=None, start_date=None, end_date=None, print_date=False):
    if dates is None:
        from mda.finance import get_download_dates
        dates = get_download_dates()
    if start_date:
        dates = sorted([d for d in dates if d >= start_date])
    if end_date:
        dates = sorted([d for d in dates if d < end_date])
    df = reduce(lambda acc, el: [
        pd.concat(acc + [read_dir(el, print_date=print_date)],
                  axis=0).drop_duplicates()],
                dates[1:],
                [read_dir(dates[0], print_date=print_date)])[0]
    return df
