import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from lagspec import nealmon
from midas_lag import mls
np.random.seed(1001)
n=250
trend = np.arange(1, n+1)
x = np.random.normal(0, 1, n*4)
z = np.random.normal(0, 1, n*12)
print(x)
fn_x = nealmon(np.array([1, -0.5]), 8)
print(fn_x)
fn_z = nealmon(np.array([2, 0.5, -0.1]), 17)
#print(np.shape(np.dot(mls(x, k_min=0, k_max=7, m=4), fn_x.T)))
#print(np.shape(np.dot(mls(z, k_min=0, k_max=16, m=12) , fn_z.T)))

y = 2 + 0.1*trend + np.dot(mls(x, k_min=0, k_max=7, m=4), fn_x.T) + np.dot(mls(z, k_min=0, k_max=16, m=12), fn_z) + np.random.normal(0, 1, n)
print(mls(x, k_min=0, k_max=7, m=4))
#print(np.shape(mls(x, k_min=0, k_max=7, m=4)))
#print(np.shape(mls(z, k_min=0, k_max=16, m=12)))
#x = trend + mls(x, k_min=0, k_max=7, m=4) + mls(z, k_min=0, k_max=16, m=12)
x = pd.concat([pd.Series(trend), pd.DataFrame(mls(x, k_min=0, k_max=7, m=4)), pd.DataFrame(mls(z, k_min=0, k_max=16, m=12))], axis=1)
print(x.head())
midas_u = LinearRegression().fit(x.iloc[1:], y[1:])
#print(midas_u.coef_)
plt.plot(y)
plt.plot(midas_u.predict(x[1:]))
plt.show()
