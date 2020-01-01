import numpy as np

def poly(x: np.array, degree: int):
    """
    Equivalent of R function poly with raw=TRUE
    Returns matrix where the first column is x and following columns are x to power i 
    for all i equal or smaller than degree
    """
    matrix = np.array(x)
    if degree > 1:
        for i in range(2, degree+1):
            x_i = x**i
            matrix = np.vstack((matrix, x_i))
    return np.transpose(matrix)


def nealmon(p: np.array, d: int):
    """

    :param p: parameters for Almon lag
    :param d: number of the coefficients
    :return: Calculate normalized exponential Almon lag coefficients given the parameters and required number of coefficients.
    """
    i = np.arange(1, d+1)
    if len(p[1:])>1:
        plc = np.sum(np.multiply(poly(i, len(p) - 1), p[1:]), axis=1)
    else:
        plc = np.multiply(poly(i, len(p) - 1), p[1:])
    return p[0] * np.exp(plc) / sum(np.exp(plc))


