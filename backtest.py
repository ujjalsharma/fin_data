import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# Importing data
HIGH = pd.read_csv('data/HIGH.csv', index_col = 'Date', parse_dates=True)
LOW = pd.read_csv('data/LOW.csv', index_col = 'Date', parse_dates=True)
OPEN = pd.read_csv('data/OPEN.csv', index_col = 'Date', parse_dates=True)
CLOSE = pd.read_csv('data/CLOSE.csv', index_col = 'Date', parse_dates=True)
VOLUME = pd.read_csv('data/VOLUME.csv', index_col = 'Date', parse_dates=True)
ADJ_CLOSE = pd.read_csv('data/ADJ_CLOSE.csv', index_col = 'Date', parse_dates=True)

# Neutrilization function
def neutralize(dframe):
    df = dframe.copy(deep=True)
    df.fillna(0, inplace=True)
    for i in range(len(df)):
        means = np.mean(df.iloc[i,:].values)
        df.iloc[i,:] = df.iloc[i,:] - means
    return df

# Rank function
def RANK(dframe):
    df = dframe.copy(deep=True)
    df.fillna(0, inplace=True)
    n = len(df.iloc[1, :])
    stp = 1/(n-1)
    rank_values = np.arange(0,1,step=stp)
    rank_values = np.append(rank_values, 1)
    
    for i in range(len(df)):
        temp1 = df.iloc[i, :]
        temp2 = df.iloc[i, :]
        for j in range(n):
            index = temp1.idxmin()
            temp2[index] = rank_values[j]
            temp1 = temp1.drop(labels=[index])
        df.iloc[i, :] = temp2
    return df


# Alpha code
def alfa(dframe):

    print('Simulation begins...')
    df = dframe.copy(deep=True)
    df.fillna(0, inplace=True)
    alpha = df.copy(deep=True)
    return_df = df.copy(deep=True)
    total_ret = df.copy(deep=True)
    price_df = CLOSE.copy(deep=True)
    turnover_df = df.copy(deep=True)
    price_df = price_df.replace(np.inf, np.nan)
    price_df.fillna(0,inplace=True)

    # Calculate value invested each day
    print('Simulation stage 1...')
    for i in range(len(df)):
        sums=np.sum(alpha.iloc[i,:].values)
        alpha.iloc[i, :] = alpha.iloc[i, :]/sums
    alpha = neutralize(alpha)
    alpha = alpha * 20000000
    alpha = alpha.replace(np.inf, np.nan)
    alpha.fillna(0, inplace=True)
    
    #calculating the change in stock price each day
    print('Simulation stage 2...')
    for i in range(1,len(df)):
        return_df.iloc[i, :] = (price_df.iloc[i, :]-price_df.iloc[i-1, :])/price_df.iloc[i-1, :]
    return_df = return_df.replace(np.inf, np.nan)
    return_df.fillna(0, inplace=True)
    
    #Calculating trading value each day
    print('Simulation stage 3...')
    for i in range(1,len(df)):
        turnover_df.iloc[i,:] = alpha.iloc[i,:]-alpha.iloc[i-1,:]
    turnover_df = turnover_df.replace(np.inf, np.nan)
    turnover_df.fillna(0, inplace=True)
    
    #Calculating returns for each day
    print('Simulation stage 4...')
    for i in range(1,len(df)):
        total_ret.iloc[i,:] = return_df.iloc[i,:]*turnover_df.iloc[i,:]
    total_ret = total_ret.replace(np.inf, np.nan)
    total_ret.fillna(0, inplace=True)
    
    #Total pnl each day
    print('Simulation stage 5...')
    total_ret['pnl'] = 0
    for i in range(1,len(df)):
        sumss=np.sum(total_ret.iloc[i,:].values)
        total_ret['pnl'].iloc[i] = sumss
    total_ret = total_ret.replace(np.inf, np.nan)
    total_ret.fillna(0, inplace=True)
    
    print('Simulation stage 6...')
    total_ret['pnl'][2:].cumsum().plot()
    print(np.sum(total_ret['pnl'].values))