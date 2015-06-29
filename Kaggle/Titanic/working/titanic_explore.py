import pandas as pd
import numpy as np
from pandas import Series, DataFrame

def load_data():
    return pd.read_table('../input/train.csv', delimiter=',')

if __name__ == '__main__':
    df = load_data()
    print pd.crosstab([df.Sex, df.Pclass], [df.Survived], margins = True)
