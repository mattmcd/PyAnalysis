from __future__ import division
import numpy as np
import pandas as pd
import urllib2
import time
import os
import re
import boto3
from tqdm import tqdm

__author__ = 'mattmcd'

dataLoc = os.path.join(os.environ.get('MDA_DATA_DIR'), 'FTSE100')
ftseFile = os.path.join(dataLoc, 'FTSE100.csv')


class LseReader:

    def __init__(self, interval=60, period=10):
        """Constructor
        :param interval: time in seconds between downloaded values
        :param period: period in days to download
        :return: LseReader
        """

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


def get_all(do_copy=False):
    """Get last 10 days of 1 minute intraday data from FTSE 100
    Args:
        do_copy: copy downloaded files to S3

    Returns:
        <none> Creates saved text files
    """
    reader = LseReader()
    download_date = time.strftime("%Y%m%d")
    save_loc = os.path.join(dataLoc, download_date)
    if not os.path.isdir(save_loc):
        os.mkdir(save_loc)
    for ticker in tqdm(reader.ftse100.ticker.values):
        try:
            txt, interval = reader.read_url(ticker)
            with open(os.path.join(save_loc, ticker + '.txt'), 'wb') as f:
                f.write(txt)
        except:
            pass
    if do_copy:
        copy_to_s3(download_date)


def get_download_dates():
    """Get list of downloaded dates
    :return: list of dates
    """
    dirs = filter(lambda s: re.match('\d{8}', s), os.listdir(dataLoc))
    return dirs


def copy_to_s3(download_date=None):
    """Copy downloaded files to S3
    :return: <none> Creates files on S3
    """
    dest_bucket = 'ftse100'
    files = os.listdir(os.path.join(dataLoc, download_date))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    if dest_bucket not in map(lambda b: b.name, s3.buckets.all()):
        bucket.create(CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    for fname in files:
        bucket.upload_file(os.path.join(dataLoc, download_date, fname),
                           'raw/' + download_date + '/' + fname)
