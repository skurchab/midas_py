import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def intrinsic_event(ts, d_up, d_down, mode='up'):
    result = []
    s_ext = None
    s_ie = None
    first_tick = True
    for i in range(len(ts)):
        s_tick = ts[i]
        if i==52:
            print(mode, s_tick, s_ext, s_ie)
        if first_tick:
            s_ext = s_tick
            s_ie = s_tick
            first_tick = False
            result.append(0)
            continue
        elif mode == 'up':
            if s_tick - s_ext >= d_up:
                mode = 'down'
                s_ext = s_tick
                s_ie = s_tick
                result.append(1)
                continue
            elif s_tick < s_ext:
                s_ext = s_tick
                if s_ie - s_ext >= d_down:
                    s_ie = s_tick
                    result.append(-2)
                    continue
                else:
                    result.append(0)
                    continue
            else:
                result.append(0)
                continue
        elif mode == 'down':
            if s_ext - s_tick >= d_down:
                mode = 'up'
                s_ext = s_tick
                s_ie = s_tick
                result.append(-1)
                continue
            elif s_tick > s_ext:
                s_ext = s_tick
                if s_ext - s_ie >= d_up:
                    s_ie = s_tick
                    result.append(2)
                    continue
                else:
                    result.append(0)
                    continue
            else:
                result.append(0)
                continue
        else:
            print(i)
            print('SOMETHING IS WRONG 1')
            exit(1)
    return np.array(result)

# Data is downloaded from https://realized.oxford-man.ox.ac.uk/data/download
data = pd.read_csv('oxford_data/realized_volatility_mod.csv', sep=';')
df = data[['DateID', 'Realized Variance (5-minute)', 'Return', 'Number of Transactions', 'Closing Price']]
df = df.rename(columns={"DateID": 'Date',
                   'Realized Variance (5-minute)': 'Variance',
                   'Number of Transactions': 'Transaction_nb',
                   'Closing Price': 'Price'})
df = df.dropna(subset = ['Price']).reset_index(drop=True)
df['Int_event'] = intrinsic_event(df['Price'], d_up=40, d_down=40, mode='up')
# Set a new Intrinsic time index
cur_index = 0
df['Int_index'] = None
for i in range(len(df)):
    if df['Int_event'][i] in [-1, 1, -2, 2]:
        cur_index = cur_index + 1
        df['Int_index'].iloc[i] = cur_index
# Transformation of time index
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='ignore')
print(df.iloc[:43])
# Data visualisation
plt.plot(df.index[:300], df.Price[:300])
plt.plot(df[(df.Int_event==1) | (df.Int_event==-1)].loc[:300].index,
         df[(df.Int_event==1) | (df.Int_event==-1)].loc[:300].Price, 'o')
plt.plot(df[(df.Int_event==2) | (df.Int_event==-2)].loc[:300].index,
         df[(df.Int_event==2) | (df.Int_event==-2)].loc[:300].Price, marker='v', linestyle='--')
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