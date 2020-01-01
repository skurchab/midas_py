import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from midas_lag import mls
x = pd.read_csv('R_data/payems.csv', encoding='ISO-8859-1', sep=';')
y = pd.read_csv('R_data/gdp_q.csv', sep=';')
yg = np.diff(np.log(y['GDP']))*100
xg = np.diff(np.log(x['PAYEMS']))*100

nx = pd.read_csv('R_data/payems_mod.csv', sep=';')
ny = pd.read_csv('R_data/gdp_q_mod.csv', sep=';')

nx.Month = nx.Month.map({'sty': 1, 'lut': 2, 'mar': 3, 'kwi': 4, 'maj': 5, 'cze': 6, 'lip': 7, 'sie': 8, 'wrz': 9, 'paz': 10, 'lis': 11, 'gru':12})
yy = ny[(ny['Year ']>=1985) & (ny['Year ']<2009)]
yy = pd.concat([yy, ny[(ny['Year ']==2009) & (ny['Quarter']=='Q1')]]).reset_index(drop=True)
print(xx)
xx = nx[(nx.Year >=1985) & (nx.Year<2009)]
xx = pd.concat([xx, nx[(nx.Year==2009) & (nx.Month <=3)]]).reset_index(drop=True)

#print(np.shape(mls(xx.Value, k_min=3, k_max=11, m=3)))
mls(yy, k_min=0, k_max=1, m=1)
#x_mu = pd.concat([pd.DataFrame(mls(yy, k_min=0, k_max=1, m=1)), pd.DataFrame(mls(xx, k_min=3, k_max=11, m=3))], axis=1)
#mls(yy, k_min=0, k_max=1, m=1)




