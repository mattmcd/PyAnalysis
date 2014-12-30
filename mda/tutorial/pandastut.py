#"10 Minutes to pandas" tutorial 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ObjectCreator:
    """Object creation demo"""
    def __init__(self):
        self.data = []

    def createSeries(self):
        s = pd.Series( [1,3,5,np.nan,6,8] );
        return s

    def createDataFrame(self):
        dates = pd.date_range('20130101', periods=6)
        df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
        return df

    def createDataFrameFromDict(self):
        data = {
            'A' : 1., 
            'B' : pd.Timestamp('20130102'), 
            'C' : pd.Series(1, index=list(range(4)), dtype='float32'),
            'D' : np.array([3] * 4, dtype='int32'),
            'E' : pd.Categorical(["test","train","test","train"]),
            'F' : 'foo' }
        df = pd.DataFrame(data);
        return df

class Viewer:
    """Example of DataFrame data viewer methods"""
    def __init__(self, df=None):
        if df is None:
            creator = ObjectCreator()
            df = creator.createDataFrame();
        self.df = df

    def all(self):
        """View all data"""
        print "All data: df"
        print self.df

    def head(self, lineCount=None):
        print "Head: df.head({})".format(lineCount)
        print self.df.head(lineCount)
    
    def tail(self, lineCount=None):
        print "Tail: df.tail({})".format(lineCount)
        print self.df.tail(lineCount)
    
    def getIndex(self, lineCount=None):
        print "Data index: df.index"
        print self.df.index
    
    def getColumns(self, lineCount=None):
        print "Data columns: df.columns"
        print self.df.columns
    
    def getValues(self, lineCount=None):
        print "Data values: df.values"
        print self.df.values
    
    def describe(self, lineCount=None):
        print "Describe data: df.describe()"
        print self.df.describe()
