import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from intrinsic_event_calc import price_intrinsic_event, intrinsic_index_calc
from data_transformation import daily_to_monthly_rr
from midas_lag import mls


# Data is downloaded from https://realized.oxford-man.ox.ac.uk/data/download
data = pd.read_csv('oxford_data/realized_volatility_mod.csv', sep=';')
df = data[['DateID', 'Realized Variance (5-minute)', 'Return', 'Number of Transactions', 'Closing Price']]
df = df.rename(columns={"DateID": 'Date',
                   'Realized Variance (5-minute)': 'Variance',
                   'Number of Transactions': 'Transaction_nb',
                   'Closing Price': 'Price'})
df = df.dropna(subset = ['Price']).reset_index(drop=True)
df['Int_event'] = price_intrinsic_event(df['Price'], d_up=40, d_down=40, mode='up')
# Set a new Intrinsic time index
df = intrinsic_index_calc(df)
# Transformation of time index
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='ignore')
# Low frequency dataframe
df_lf = daily_to_monthly_rr(df)
print(df_lf.head())
# It is assumed that the numbers of observations of different frequencies match exactly
# through the frequency ratio (ni = nmi)
# In our case assumption is not satisfied
#print(len(df_lf), len(df))

#It can be noticed that last december has only two datapoints
#for year in  df.Date.dt.year.unique():
    #for month in df[df.Date.dt.year==year].Date.dt.month.unique():
        #print(year, month)
        #print(len(df[(df.Date.dt.year==year) & (df.Date.dt.month==month)].Date.dt.day.unique()))

df_dec = pd.DataFrame(columns=list(df))
df_dec['Date'] = [df.Date.max() + datetime.timedelta(days=x) for x in range(19)][1:]
df = pd.concat([df, df_dec]).reset_index(drop=True)
#print(len(df_lf), len(df))
df_equal = pd.DataFrame(columns=list(df))
for year in  df.Date.dt.year.unique():
    for month in df[df.Date.dt.year==year].Date.dt.month.unique():

        df_equal = pd.concat([df_equal, df[(df.Date.dt.year==year) &
                                               (df.Date.dt.month==month)].iloc[:15]]).reset_index(drop=True)
#print(len(df_lf), len(df_equal))
#print(df_equal.head())
mls_ = pd.DataFrame(mls(df_equal.Return, k_min=0, k_max=180, m=15))
print(np.shape(mls_), len(df_lf))
#print(mls_.tail())
#print(df.iloc[:43])

#TRAIN
df_lf_tr = df_lf[df_lf.Date.dt.year < 2017].reset_index(drop=True)
df_tr = df_equal[df_equal.Date.dt.year < 2017].reset_index(drop=True)
print(mls(df_tr.Return, k_min=0, k_max=180, m=15))

# Data visualisation
plt.plot(df.index[:300], df.Price[:300], label='Original time series')
plt.plot(df[(df.Int_event==1) | (df.Int_event==-1)].loc[:300].index,
         df[(df.Int_event==1) | (df.Int_event==-1)].loc[:300].Price, 'o', label='Directional change events')
plt.plot(df[(df.Int_event==2) | (df.Int_event==-2)].loc[:300].index,
         df[(df.Int_event==2) | (df.Int_event==-2)].loc[:300].Price, marker='v', linestyle='--', label='Overshooot intrinsic events')
plt.ylabel('Price')
plt.xlabel('Time index')
plt.legend()
plt.show()


#fig, axs = plt.subplots(2, 2)
#axs[0, 0].hist(df.Variance, bins=50, log=True)
#axs[0, 0].hist(df[(df.Int_event==1) | (df.Int_event==-1)].Variance, bins=50, log=True)
#axs[0, 0].set_title('Variance')
#axs[0, 1].hist(df.Return, bins=50, log=True)
#axs[0, 1].hist(df[(df.Int_event==1) | (df.Int_event==-1)].Return, bins=50, log=True)
#axs[0, 1].set_title('Return')
#axs[1, 0].hist(df.Price, bins=50, log=True)
#axs[1, 0].hist(df[(df.Int_event==1) | (df.Int_event==-1)].Price, bins=50, log=True)
#axs[1, 0].set_title('Closing Price')
#axs[1, 1].hist(df.Transaction_nb, bins=50, log=True)
#axs[1, 1].hist(df[(df.Int_event==1) | (df.Int_event==-1)].Transaction_nb, bins=50, log=True)
#axs[1, 1].set_title('Number of Transactions')
#plt.show()

#fig, axs = plt.subplots(2, 2)
#axs[0, 0].plot(df.Variance)
#axs[0, 0].set_title('Variance')
#axs[0, 1].plot( df.Return)
#axs[0, 1].set_title('Return')
#axs[1, 0].plot(df.Price)
#axs[1, 0].plot(df[(df.Int_event==1) | (df.Int_event==-1)].Price, 'o', ms=0.5)
#axs[1, 0].set_title('Closing Price')
#axs[1, 1].plot(df.Transaction_nb)
#axs[1, 1].set_title('Number of Transactions')
#plt.show()

#fig, axs = plt.subplots(2, 2)
#axs[0, 0].plot(df[(df.Int_event==1) | (df.Int_event==-1)].Variance)
#axs[0, 0].set_title('Variance')
#axs[0, 1].plot( df[(df.Int_event==1) | (df.Int_event==-1)].Return)
#axs[0, 1].set_title('Return')
#axs[1, 0].plot(df[(df.Int_event==1) | (df.Int_event==-1)].Price)
#axs[1, 0].set_title('Closing Price')
#axs[1, 1].plot(df[(df.Int_event==1) | (df.Int_event==-1)].Transaction_nb)
#axs[1, 1].set_title('Number of Transactions')
#plt.show()