from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

kaggleRoot = '/home/mattmcd/Work/Projects/PyCharm/PyAnalysis/Kaggle/'
kaggleComp = 'CouponPurchasePrediction/'
os.chdir(kaggleRoot + kaggleComp + 'working')

__author__ = 'mattmcd'


def get_all_data():
    def dataloc(name):
        return kaggleRoot + kaggleComp + 'input/' + name

    def readdata(name):
        df = pd.read_csv(dataloc(name + '.csv'))
        # Convert date columns
        date_cols = ['DISPFROM', 'DISPEND', 'VALIDFROM', 'VALIDEND', 'I_DATE',
                     'REG_DATE', 'WITHDRAW_DATE']
        for col in filter(lambda c: c in date_cols, df.columns):
            df[col] = pd.to_datetime(df[col])
        return df

    # Import the data into dataframe objects
    cp_detail_train = readdata('coupon_detail_train')
    cp_list_train = readdata('coupon_list_train')
    cp_list_test = readdata('coupon_list_test')
    user_list = readdata('user_list')
    cp_area_train = readdata('coupon_area_train')
    cp_area_test = readdata('coupon_area_test')
    cp_visit_train = readdata('coupon_visit_train')
    data = {'train':
                {'cp_list': cp_list_train, 'cp_detail': cp_detail_train, 'cp_area': cp_area_train,
                 'cp_visit' : cp_visit_train},
            'test':
                {'cp_list': cp_list_test, 'cp_area': cp_area_test},
            'user': user_list}
    data['train']['cp_visit'] = (data['train']['cp_visit'][['VIEW_COUPON_ID_hash', 'USER_ID_hash']]
                                 [data['train']['cp_visit']['PURCHASE_FLG'] != 1])
    return data


def create_coupon_categoricals(df):
    """Convert columns of coupon list to categorical vectors"""
    df['VALIDPERIOD'] = df['VALIDPERIOD'].fillna(-1)
    df['VALIDPERIOD'] += 1
    df.loc[df['VALIDPERIOD'] > 1, 'VALIDPERIOD'] = 1
    df['USABLE_DATE_SUM'] = (
        df[['USABLE_DATE_' + x for x in
            ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT','SUN','HOLIDAY', 'BEFORE_HOLIDAY']]]
        > 0).astype(int).sum(axis=1)
    return df


data = get_all_data()
data['train']['cp_list'] = create_coupon_categoricals(data['train']['cp_list'])
data['test']['cp_list'] = create_coupon_categoricals(data['test']['cp_list'])

cp_df = data['train']['cp_list']
pu_df = data['train']['cp_detail']
users = np.unique(pu_df['USER_ID_hash'].values)
get_user_purchases = lambda ind: cp_df[np.in1d(cp_df['COUPON_ID_hash'], pu_df['COUPON_ID_hash'][np.in1d(pu_df['USER_ID_hash'], users[ind])])]

train = pd.merge(data['train']['cp_detail'], data['train']['cp_list'])
train = train[["COUPON_ID_hash","USER_ID_hash","GENRE_NAME","DISCOUNT_PRICE",
               "DISPPERIOD","large_area_name","small_area_name","VALIDPERIOD","USABLE_DATE_SUM"]]

# append test set to the training set for model.matrix factor column
# conversion
data['test']['cp_list']['USER_ID_hash'] = "dummyuser"
cpchar = data['test']['cp_list'][["COUPON_ID_hash","USER_ID_hash",
                   "GENRE_NAME","DISCOUNT_PRICE","DISPPERIOD",
                   "large_area_name","small_area_name","VALIDPERIOD","USABLE_DATE_SUM"]]
train = pd.concat([train,cpchar])

#NA imputation to values of 1
train.fillna(1)
#feature engineering
train.DISCOUNT_PRICE = 1/np.log10(train.DISCOUNT_PRICE)
train.loc[train.DISPPERIOD>7, 'DISPPERIOD'] = 7
train.DISPPERIOD /= 7
train.USABLE_DATE_sum /= 9

