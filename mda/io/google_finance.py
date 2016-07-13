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
        df = parse_text(txt, interval)
        return df


def parse_text(txt, interval, ticker=None):
    lines = txt.split('\n')
    cols = lines[4].lower().split('=')[1].split(',')
    recs = [dict(zip(cols, line.split(','))) for line in lines[7:-1]]
    df = pd.DataFrame(recs, columns=cols)
    for col in cols[1:]:
        df[col] = pd.to_numeric(df[col])
    dates = np.zeros(df.date.shape, dtype=pd.Timestamp)
    last_date = pd.Timestamp(0)
    for i, date_str in enumerate(df.date):
        if not date_str:
            continue
        if date_str[0].lower() == 'a':
            last_date = pd.to_datetime(int(date_str[1:]), unit='s')
            dates[i] = last_date
        else:
            # Offset
            this_date = last_date + pd.to_timedelta(int(date_str) * interval, unit='s')
            dates[i] = this_date
    df['date'] = dates
    if ticker:
        df['ticker'] = ticker

    return df


def read_file(ticker_file, datestr, interval=60):
    with open(mda.data_dir('FTSE100', datestr, ticker_file)) as f:
        return parse_text(f.read(), interval, ticker=ticker_file.split('.')[0])


def read_dir(datestr, interval=60):
    return pd.concat(
        [read_file(f, datestr, interval)
         for f in os.listdir(mda.data_dir('FTSE100', datestr))])
