import IPython

ipython = IPython.get_ipython()
ipython.magic('load_ext autoreload')
ipython.magic('autoreload 2')

# Useful imports in console
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import boto3


pd.set_option('display.expand_frame_repr', False)
