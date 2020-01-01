import sys
import numpy as np
def mls(x: np.array, k_min: int, k_max: int,  m: int):
    """
    stacks a HF data vector x into a corresponding matrix of observations at LF
     of size dim x / m x dim k: from the first to the last HF lag defined by vector k
    """
    n_x = len(x)
    n = n_x // m
    #print(n)
    lk = np.arange(k_min, k_max) #???
    k = k_max + 1
    if k_min > 0:
        k_min = 0
    if n_x % m != 0:
        print("Incomplete high frequency data")
        sys.exit(1)
    idx = m*(np.arange((k-1)//m+1, (n-k_min+1)))
    array = np.arange(k_min, k)
    X = []
    for i in array:
        X.append(x[idx-array[i]])
    #print(X)
    X = np.array(X).T
    #print(X)
    #print(X.shape[0])
    if  n-X.shape[0]>0:
        padd = np.empty((n-X.shape[0], X.shape[1]))
        padd[:] = np.nan
        res = np.concatenate((padd, X))
    else:
        res = X
    #print(res)
    return res

#print(mls(np.arange(1,17), 0, 8, 2))


