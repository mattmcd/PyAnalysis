from __future__ import division
import numpy as np
import pandas as pd
import urllib2

# __author__ = 'mattmcd'


class LseReader:

    def __init__(self):
        dataLoc = '/home/mattmcd/Work/Data/'
        ftseFile =  dataLoc + 'FTSE100.csv'

        self.ftse100 = pd.read_csv( ftseFile )
        self.prefixURL = 'https://www.google.com/finance/getprices?'

    def read_history(self, ticker, interval=300, period=10):
        """Read intraday history for selected ticker on LSE"""
        txt = urllib2.urlopen(self.prefixURL +
                              'q={Ticker}&x=LON&i={Interval}&p={Period}d&f=d,o,h,l,c,v'.format(
            Ticker=ticker, Interval=interval, Period=period)).read()
        return txt
