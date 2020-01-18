import numpy as np
import pandas as pd

def daily_to_monthly_rr(df: pd.DataFrame):

    """Function returns dataframe with monthly rr calculated basing on daily price data

    df - dataframe with daily price data
    Columns: Date, Price are required

   The arithmetic monthly return is equal to P(t+1) / P(t) -1
   where P(t+1) is the value of the index at the end of month t
   and P(t) the value of the index at the end of month (t-1).

   I'm not sure whether variance is computed correctly
    """

    df_lf = pd.DataFrame(columns=['Date', 'Return'])
    returns = []
    dates = []
    years = []
    variance = []
    for year in df.Date.dt.year.unique():
        for month in df[df.Date.dt.year==year].Date.dt.month.unique():
            if month==1:
                if years:
                    max_month = df[df.Date.dt.year==years[-1]].Date.dt.month.max()
                    max_date = df[(df.Date.dt.year==years[-1]) & (df.Date.dt.month==max_month)].Date.dt.day.max()
                    pt = df[(df.Date.dt.year==years[-1]) &
                            (df.Date.dt.month==max_month)&
                            (df.Date.dt.day==max_date)].Price.values[0]
                    max_date_1 = df[(df.Date.dt.year==year)&
                                    (df.Date.dt.month==month)].Date.dt.day.max()
                    pt_1 = df[(df.Date.dt.year==year)&
                              (df.Date.dt.month==month)&
                              (df.Date.dt.day==max_date_1)].Price.values[0]
                    variance.append(np.var(df[df.Date.between('{}-{}-{}'.format(years[-1], max_month, max_date),
                                                              '{}-{}-{}'.format(year, month, max_date_1))].Return))
                    #print(df[df.Date.between('{}-{}-{}'.format(years[-1], max_month, max_date), '{}-{}-{}'.format(year, month, max_date_1))])
                    returns.append((pt_1/pt - 1))

                else:
                    returns.append(None)
                    variance.append(None)
            else:
                max_date = df[(df.Date.dt.year == year) &
                              (df.Date.dt.month == month-1)].Date.dt.day.max()
                pt = df[(df.Date.dt.year==year)&
                        (df.Date.dt.month==month-1)&
                        (df.Date.dt.day==max_date)].Price.values[0]
                max_date_1 = df[(df.Date.dt.year == year) &
                                (df.Date.dt.month == month)].Date.dt.day.max()
                pt_1 = df[(df.Date.dt.year == year) &
                          (df.Date.dt.month == month) &
                          (df.Date.dt.day == max_date_1)].Price.values[0]
                returns.append((pt_1 / pt - 1))
                variance.append(np.var(df[df.Date.between('{}-{}-{}'.format(year, month-1, max_date), '{}-{}-{}'.format(year, month, max_date_1))].Return))


            dates.append('{}{}'.format(year, month))
        years.append(year)

    df_lf['Variance'] = np.array(variance)
    df_lf['Return'] = np.array(returns)
    df_lf['Date'] = np.array(dates)
    df_lf['Date'] = pd.to_datetime(df_lf['Date'], format='%Y%m', errors='ignore')

    return df_lf