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


def update_local(download_date):
    """Update local cache of data
    Parameters
    ----------
    download_date

    Returns
    -------

    """
    s3 = get_s3(download_date)
    s3.get()


def get_download_dates():
    """Get list of downloaded dates
    :return: list of dates
    """
    dirs = sorted(filter(lambda s: re.match('\d{8}', s), os.listdir(dataLoc)))
    return dirs


def plot_returns(df=None, date=None, base_ind=0, n=10):
    """Plot return index from closing price time series for top/bottom n stocks

    Parameters
    ----------
    df: ohlc stock data
    date: date to retrieve if stock data not present
    base_ind: row index to use for normalizing prices, default 0
    n: top/bottom n stocks will be plotted

    Returns
    -------

    """
    import numpy as np
    if df is None:
        from mda.io.google_finance import read_dir
        df = read_dir(date)

    px_close = df.set_index(['date', 'ticker'])['close'].unstack()
    returns = px_close.pct_change().fillna(0)
    ret_index = (1 + returns).cumprod()
    ret_index = ret_index.div(ret_index.iloc[base_ind, :], axis=1)
    px_end = ret_index.iloc[-1, :].sort_values(ascending=False)
    top_bottom = np.append(px_end.index[:n].values,
                           px_end.index[-n:].values)

    ret_index.reset_index()[top_bottom].plot()