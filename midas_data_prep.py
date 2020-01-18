import pandas as pd
import numpy as np
from midas_lag import mls
from data_transformation import daily_to_monthly_rr
from sklearn.linear_model import LinearRegression


data = pd.read_csv('oxford_data/realized_volatility_mod.csv', sep=';')
df = data[['DateID', 'Realized Variance (5-minute)', 'Return', 'Number of Transactions', 'Closing Price']]
df = df.rename(columns={"DateID": 'Date',
                   'Realized Variance (5-minute)': 'Variance',
                   'Number of Transactions': 'Transaction_nb',
                   'Closing Price': 'Price'})
df = df.dropna(subset = ['Price']).reset_index(drop=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='ignore')
df['Year'] = df.Date.dt.year
df['Month'] = df.Date.dt.month
df = df.iloc[:-2]
print(len(df))
min_days = 23
df_mod = pd.DataFrame(columns=list(df))
for year in df.Year.unique():
    df_y = df[df.Year == year]
    for month in df_y.Month.unique():
        df_m = df_y[df_y.Month == month]
        if len(df_m) < min_days:
            if month != 1:
                df_m_add = df_y[df_y.Month == month-1].iloc[-(min_days-len(df_m)):]
            else:
                df_m_add = df[(df.Year==year-1) & (df.Month==12)].iloc[-(min_days-len(df_m)):]
            df_m_add['Month'] = month
            df_m_add['Year'] = year
            df_m = pd.concat([df_m_add, df_m])
                #print(df_m_add)
        df_mod = df_mod.append(df_m)

df_mod = df_mod.iloc[df_mod[(df_mod.Month==1) & (df_mod.Year==2000)].index.max()+1:].reset_index(drop=True)
for year in df_mod.Year.unique():
    df_y = df_mod[df_mod.Year == year]
    for month in df_y.Month.unique():
        df_m = df_y[df_y.Month == month]
        if len(df_m) < min_days:
            print(df_m)

mls_ = pd.DataFrame(mls(df_mod.Date.dt.date, k_min=0, k_max=252, m=23))
print(mls_.iloc[:20])
print(mls_.tail())
print(np.shape(mls_.iloc[10:]))
df_lf = daily_to_monthly_rr(df).iloc[1:].reset_index(drop=True)
print(np.shape(mls_.iloc[10:]), np.shape(df_lf.iloc[10:]))
print(df_lf.iloc[10:12])

x_mu = pd.DataFrame(mls(df_mod.Return**2, k_min=0, k_max=252, m=23))
midas_u = LinearRegression().fit(x_mu.iloc[10:], df_lf.Variance.iloc[10:])
print(midas_u.coef_)