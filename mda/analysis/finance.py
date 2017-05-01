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
    import numpy as np
    if df is None:
        from mda.io.google_finance import read_dir
        df = read_dir(date)

    ret_index = calc_return_index(df, base_ind=base_ind)
    px_end = ret_index.iloc[-1, :].sort_values(ascending=False)
    top_bottom = np.append(px_end.index[:n].values,
                           px_end.index[-n:].values)

    ret_index.reset_index()[top_bottom].plot()