import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append(os.environ.get('MDA_CODE_DIR'))
import mda


def read():
    df = pd.concat(
        pd.read_csv(
            mda.data_dir(
                'doing_data_science', 'dds_datasets', 'nyt{}.csv'.format(i)),
        ).assign(Day=i) for i in range(1, 32))
    df.columns = [col.lower() for col in df.columns]
    return df


def transform(df):
    df['age_group'] = pd.cut(df.age, [-np.inf, 0, 18, 24, 34, 44, 54, 64, np.inf], include_lowest=False)
    return df


def analyse(df):
    df_g = df.groupby(['day', 'age_group'])[['impressions', 'clicks']].sum()
    df_g['ctr'] = df_g['clicks'].div(df_g['impressions'])


def visualize(df):
    # Clicks by day and gender
    df.query('signed_in == 1').pivot_table(values='clicks', index='day', columns='gender', aggfunc='sum').plot()
    # Impressions by day and gender
    df.query('signed_in == 1').pivot_table(values='impressions', index='day', columns='gender', aggfunc='sum').plot()

    # Click Through Rate by day and gender
    df.query('signed_in == 1').pivot_table(values='clicks', index='day', columns='gender', aggfunc='sum').div(
        df.query('signed_in == 1').pivot_table(values='impressions', index='day', columns='gender',
                                               aggfunc='sum')).plot()

    # Click Through Rate by day and age group
    df.query('signed_in == 1').pivot_table(values='clicks', index='day', columns='age_group', aggfunc='sum').div(
        df.query('signed_in == 1').pivot_table(values='impressions', index='day', columns='age_group',
                                               aggfunc='sum')).plot()

    # Click Through Rate by age group and gender
    df.query('signed_in == 1').pivot_table(values='clicks', index='age_group', columns='gender', aggfunc='sum').div(
        df.query('signed_in == 1').pivot_table(values='impressions', index='age_group', columns='gender',
                                               aggfunc='sum')).plot()


if __name__ == '__main__':
    df = read()
    df = transform(df)
    visualize(df)
