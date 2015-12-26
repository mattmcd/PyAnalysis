from __future__ import division
import numpy as np
import pandas as pd
import urllib2
import time
import os
from tqdm import tqdm

__author__ = 'mattmcd'


class LseReader:

    def __init__(self, interval=60, period=10):
        """Constructor
        :param interval: time in seconds between downloaded values
        :param period: period in days to download
        :return: LseReader
        """
        dataLoc = '/home/mattmcd/Work/Data/FTSE100'
        ftseFile = dataLoc + 'FTSE100.csv'

        self.ftse100 = pd.read_csv( ftseFile )
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


def parse_text(txt, interval):
    lines = txt.split('\n')
    cols = lines[4].lower().split('=')[1].split(',')
    recs = [dict(zip(cols, line.split(','))) for line in lines[7:-1]]
    df = pd.DataFrame(recs, columns=cols)
    df[cols[1:]] = df[cols[1:]].convert_objects(convert_numeric=True)
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
            this_date = last_date + pd.to_timedelta(int(date_str)*interval, unit='s')
            dates[i] = this_date
    df['date'] = dates
    df.index = df.date

    return df


def get_all():
    """Get last 10 days of 1 minute intraday data from FTSE 100
    :return: <none> Creates saved text files
    """
    reader = LseReader()
    save_loc = ('/home/mattmcd/Work/Data/FTSE100/' + time.strftime("%Y%m%d") + '/')
    if not os.path.isdir(save_loc):
        os.mkdir(save_loc)
    for ticker in tqdm(reader.ftse100.Ticker.values):
        try:
            txt, interval = reader.read_url(ticker)
            with open(save_loc + ticker + '.txt', 'wb') as f:
                f.write(txt)
        except:
            pass


if __name__ == "__main__":
    reader = LseReader()
    tickers = reader.ftse100.Ticker
    df = reader.read_history(tickers[0])
