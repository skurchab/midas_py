import numpy as np
import pandas as pd

def price_intrinsic_event(ts: pd.Series, d_up: int, d_down: int, mode='up'):
    """Function is written basing on 'Agent-Based Model in Directional-Change Intrinsic Time' by Petrov and Golub pseudo-code """
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

def intrinsic_index_calc(df: pd.DataFrame):

    """Can be applied on the df transformed by price_intrinsic_event() function """

    cur_index = 0
    df['Int_index'] = None
    df['Int_index'].iloc[0] = cur_index
    for i in range(len(df)):
        if df['Int_event'][i] in [-1, 1, -2, 2]:
            cur_index = cur_index + 1
            df['Int_index'].iloc[i] = cur_index

    return df
