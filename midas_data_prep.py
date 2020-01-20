import pandas as pd
import numpy as np
from midas_lag import mls
from data_transformation import daily_to_monthly_rr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# In the document the procedure of application of unrestricted MIDAS regression on
# real-life data is presented

# READ AND PREPROCESS the REAL_LIFE DATA
# Data source: https://realized.oxford-man.ox.ac.uk/data/download
data = pd.read_csv('oxford_data/realized_volatility_mod.csv', sep=';')
df = data[['DateID', 'Realized Variance (5-minute)', 'Return', 'Number of Transactions', 'Closing Price']]
df = df.rename(columns={"DateID": 'Date',
                        'Realized Variance (5-minute)': 'Variance',
                        'Number of Transactions': 'Transaction_nb',
                        'Closing Price': 'Price'})
df = df.dropna(subset=['Price']).reset_index(drop=True)
# DATEINDEX COLUMN INTO THE DATE OF RIGHT FORMAT
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='ignore')
# ADD NEW COLUMNS (in order to make further navigation in dataset easier)
df['Year'] = df.Date.dt.year
df['Month'] = df.Date.dt.month
# REMOVE LAST TWO RAWS OF THE DATASET AS DECEMBER  OF THE LAST YEAR HAS ONLY TWO RECORDS
df = df.iloc[:-2]
# INITIAL LENGTH OF THE DATASET CAN NOT BE DIVIDED BY NEITHER 23 NOR 22
print(len(df))
# WE REPEAT SOME RECORDS IN ORDER TO HAVE EXACTLY min_days=23 RECORDS CORRESPONDING TO 1 MONTH
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
                df_m_add = df[(df.Year == year-1) & (df.Month == 12)].iloc[-(min_days-len(df_m)):]
            df_m_add['Month'] = month
            df_m_add['Year'] = year
            df_m = pd.concat([df_m_add, df_m])
        df_mod = df_mod.append(df_m)
# REMOVE FIRST MONTH OF THE FIRST YEAR  AS WE DO NOT HAVE THIS RECORD IN LAW FREQUENCY DATASET
df_mod = df_mod.iloc[df_mod[(df_mod.Month == 1) & (df_mod.Year == 2000)].index.max()+1:].reset_index(drop=True)
# CHECK WHETHER EACH MONTH HAS EQUAL AMOUNT OD DAYS
for year in df_mod.Year.unique():
    df_y = df_mod[df_mod.Year == year]
    for month in df_y.Month.unique():
        df_m = df_y[df_y.Month == month]
        if len(df_m) < min_days:
            print(df_m)
# CHECK THE DISTRIBUTION OF DATES AFTER THE MLS PROCEDURE APPLIED ON FULL DATA
mls_ = pd.DataFrame(mls(df_mod.Date.dt.date, k_min=0, k_max=252, m=23))
# print(mls_.iloc[20:])
df_lf = daily_to_monthly_rr(df).iloc[1:].reset_index(drop=True)
# FIT THE MODEL TO THE FULL DATASET AND CHECK THE COEFICIENTS
x_mu = pd.DataFrame(mls(df_mod.Return**2, k_min=0, k_max=252, m=23))
midas_u = LinearRegression().fit(x_mu.iloc[10:], df_lf.Variance.iloc[10:])
# print(midas_u.coef_)
# TRAIN - TEST SETS
# second restriction in order remove the dubled december in the last year
data_train = df_mod[(df_mod.Date <= '2010-12-31') & (df_mod.Year <= 2010)]
df_lf_train = df_lf[df_lf.Date <= '2010-12-31']
data_test = df_mod[df_mod.Year >= 2011].reset_index(drop=True)
df_lf_test = df_lf[df_lf.Date >= '2011-01-01'].reset_index(drop=True)
print('Train: {}, Test: {}'.format(len(data_train), len(data_test)))
x_mu_train = pd.DataFrame(mls(data_train.Return**2, k_min=0, k_max=252, m=23))
x_mu_test = pd.DataFrame(mls(data_test.Return**2, k_min=0, k_max=252, m=23))
# MODEL FIT & PREDICT
midas_u_tr = LinearRegression().fit(x_mu_train.iloc[10:], df_lf_train.Variance.iloc[10:])
print(np.around(midas_u_tr.coef_, 3))
# print(pd.DataFrame(mls(data_test.Date.dt.date, k_min=0, k_max=252, m=23)).iloc[:20])
y_pred = midas_u_tr.predict(x_mu_test.iloc[10:])

print(r2_score(y_pred, df_lf_test.Variance[10:].reset_index(drop=True)))
plt.plot(y_pred, 'o', label='pred')
plt.plot(df_lf_test.Variance[10:].reset_index(drop=True), 'o', label='test')
plt.show()



