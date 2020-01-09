import pandas as pd
import matplotlib.pyplot as plt
from intrinsic_event_calc import price_intrinsic_event, intrinsic_index_calc
from data_transformation import daily_to_monthly_rr


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

print(df.iloc[:43])
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