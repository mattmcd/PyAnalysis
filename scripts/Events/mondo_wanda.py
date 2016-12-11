import numpy as np
import pandas as pd
import mda
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_pickle(mda.data_dir('Events_20161207_20161208.pkl'))
sessions = df.groupby('session_id')['collector_tstamp'].agg(['min', 'max'])
sessions['duration'] = (sessions['max'] - sessions['min'])/pd.Timedelta(1, 's')
sessions = pd.merge(sessions, df[['session_id', 'app_id']].drop_duplicates(), left_index=True, right_on='session_id')
sessions.loc[sessions.app_id == 'phone', 'app'] = 'Wanda'
sessions.loc[sessions.app_id.str.contains('mondo'), 'app'] = 'Mondo'

g = sns.FacetGrid(sessions.query('10 < duration < 600'), col='app')
g.map(plt.hist, 'duration', normed=True)

df = pd.merge(df, sessions)
df['t'] = (df['collector_tstamp'] - df['min'])/pd.Timedelta(1, 's')

df.loc[df.se_category.str.contains('TryItClick'), 'event'] = 1

g = sns.FacetGrid(df.query('t < 600'), row='app')
g.map(plt.scatter, 't', 'event', alpha=0.05)

g = sns.FacetGrid(df.query('event == 1 and t < 600'), row='app')
g.map(plt.hist, 't', normed=True)
