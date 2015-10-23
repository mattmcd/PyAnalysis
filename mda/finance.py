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
        lines = txt.split('\n')
        cols = lines[4].lower().split('=')[1].split(',')
        recs  = [dict(zip(cols, line.split(','))) for line in lines[7:-1]]
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


reader = LseReader()
tickers = reader.ftse100.Ticker
df = reader.read_history(tickers[0])