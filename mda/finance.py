from __future__ import division

import os
import re
import time
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
        proxy_args = {
            'bucket': 'ftse100',
            'local_dir': mda.data_dir('FTSE100', download_date),
            'prefix': 'raw/' + download_date + '/'
        }
        s3 = S3Proxy(**proxy_args)
        s3.put()


def get_download_dates():
    """Get list of downloaded dates
    :return: list of dates
    """
    dirs = filter(lambda s: re.match('\d{8}', s), os.listdir(dataLoc))
    return dirs
