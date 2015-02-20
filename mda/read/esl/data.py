import urllib2
from StringIO import StringIO
import pandas as pd

def read(name, sep=','):
    baseURL = 'http://statweb.stanford.edu/~tibs/ElemStatLearn/datasets/'
    req = urllib2.Request( baseURL + name + '.data' )
    response = urllib2.urlopen( req )
    ds = pd.read_csv( StringIO( response.read()), sep)
    return ds
