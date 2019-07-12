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

# Basic operation
def subtract(df1, df2):
    dfs = df1.copy(deep=True)
    for i in range(2590):
        dfs.iloc[i,:] = df1.iloc[i,:]-df2.iloc[i,:] 
    return dfs

def add(df1, df2):
    dfs = df1.copy(deep=True)
    for i in range(2590):
        dfs.iloc[i,:] = df1.iloc[i,:]+df2.iloc[i,:]
    return dfs

def multiply(df1, df2):
    dfs = df1.copy(deep=True)
    for i in range(2590):
        dfs.iloc[i,:] = df1.iloc[i,:]*df2.iloc[i,:]
    return dfs

def divide(df1, df2):
    dfs = df1.copy(deep=True)
    for i in range(2590):
        dfs.iloc[i,:] = df1.iloc[i,:]/df2.iloc[i,:]
    return dfs



# Alpha code
def alpha(df):
    df = df.fillna(0)
    alpha = df.copy(deep=True)
    return_df = df.copy(deep=True)
    total_ret = df.copy(deep=True)
    
    alpha['sum'] = 0
    
    for i in range(2590):
        sums=np.sum(alpha.iloc[i,:].values)
        alpha['sum'].iloc[i] = sums
        alpha.iloc[i, :] = alpha.iloc[i, :]/sums
    
    for i in range(1,2590):
        return_df.iloc[i, :] = return_df.iloc[i, :]-return_df.iloc[i-1, :]
    
    alpha = alpha * 20000000
    
    for i in range(1,2590):
        total_ret.iloc[i,:] = alpha.iloc[i,:]*return_df.iloc[i,:]
    
    total_ret['pnl'] = 0
    for i in range(1,2590):
        sums=np.sum(total_ret.iloc[i,:].values)
        total_ret['pnl'].iloc[i] = sums
    
    total_ret['pnl'][64:].cumsum().plot()