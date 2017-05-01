from __future__ import division

import os
import re
import time

import boto3
from tqdm import tqdm

import mda
from mda.io.google_finance import LseReader
from mda.io.s3 import S3Proxy

__author__ = 'mattmcd'

dataLoc = mda.data_dir('FTSE100')


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
        s3 = get_s3(download_date)
        s3.put()


def get_s3(download_date):
    proxy_args = {
        'bucket': 'ftse100',
        'local_dir': mda.data_dir('FTSE100', download_date),
        'prefix': 'raw/' + download_date + '/'
    }
    s3 = S3Proxy(**proxy_args)
    return s3


def update_local(download_date=None):
    """Update local cache of data
    Parameters
    ----------
    download_date: YYYYMMDD date to retrieve from S3
        If None defaults to retrieving all dates not present in local cache

    Returns
    -------

    """
    if download_date is None:
        local_dates = get_download_dates()
        remote_dates = get_download_dates(local=False)
        missing_dates = set(remote_dates) - set(local_dates)
        for date in tqdm(missing_dates):
            update_local(date)
    else:
        s3 = get_s3(download_date)
        s3.get()


def get_download_dates(local=True):
    """Get list of downloaded dates
    :return: list of dates
    """
    if local:
        dates = sorted(filter(
            lambda s: re.match('\d{8}', s), os.listdir(dataLoc)))
    else:
        # Get download dates from S3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('ftse100')
        lst = bucket.objects.filter(Prefix='raw')
        dates = sorted([item.key.split('/')[1] for item in lst])
    return dates
