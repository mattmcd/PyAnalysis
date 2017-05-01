import numpy as np
import pandas as pd


def normalize_periods(df):
    """Normalize number of intervals since market open
       Assume first full minute of trading on LSE finishes at 08:01 local time.
       (Original Google data uses number of intervals since first timestamp for a stock,
       which occasionally can be 08:00)
    
    Args:
        df: dataframe of OHLC data.  Must have date and tz_offset (minutes) columns

    Returns:
        None, modifies dataframe argument
    """
    df['period'] = (
        df.date - (
            df.date.dt.floor('D') + pd.Timedelta(8, 'h') + pd.Timedelta(60, 's') -
            df.tz_offset.map(lambda x: pd.Timedelta(x, 'm')))) / pd.Timedelta(1, 'm')


def fraction_traded(df_in, cumulative=False):
    """Trading volume in each stock in terms of overall value traded
    
    Args:
        df_in: OHLC data
        cumulative: use cumulative traded value instead of considering each interval 
            Default False

    Returns:
        df_frac_traded - fraction of trading that each stock's traded value represents 
    """
    df = df_in.reset_index().copy()
    df.set_index(['date', 'period', 'ticker'], inplace=True)
    df['value_traded'] = df.close * df.volume / 100
    df_traded = df.value_traded.unstack().fillna(0)
    if cumulative:
        # Cumulative value traded
        df_traded = df_traded.cumsum()
    df_frac_traded = pd.DataFrame(df_traded.values / df_traded.sum(axis=1).values[:, None], index=df_traded.index,
                                  columns=df_traded.columns)
    df_frac_traded.fillna(0, inplace=True)
    return df_frac_traded


def calc_return_index(df, base_ind=0):
    """Convert price indexes into return index normalized to some base row
    Parameters
    ----------
    df: dataframe of ohlc data
    base_ind: row index to use for normalizing prices, default 0

    Returns
    -------
    dataframe of price indexes normalized by return
    """
    px_close = df.set_index(['date', 'ticker'])['close'].unstack()
    returns = px_close.pct_change().fillna(0)
    ret_index = (1 + returns).cumprod()
    ret_index = ret_index.div(ret_index.iloc[base_ind, :], axis=1)
    return ret_index


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
    if df is None:
        from mda.io.google_finance import read_dir
        df = read_dir(date)

    ret_index = calc_return_index(df, base_ind=base_ind)
    px_end = ret_index.iloc[-1, :].sort_values(ascending=False)
    top_bottom = np.append(px_end.index[:n].values,
                           px_end.index[-n:].values)

    ret_index.reset_index()[top_bottom].plot()
