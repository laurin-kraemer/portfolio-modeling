# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:51:38 2021

@author: LK
"""

import pandas as pd
import yfinance as yf
import numpy as np

# Get List of S&P 500 companies and save them in a Dataframe

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
data = table[0]
sp500_components = pd.DataFrame(data=data, columns=['Symbol'])


# Initialize Ticker objects

arange = np.arange(len(sp500_components))
for i in arange:
    sp500_components.loc[i, 'Ticker'] = yf.Ticker(sp500_components.loc[i, 'Symbol'])

# Loop over all ticker-symbols in S&P 500

for i in np.arange(len(sp500_components)):
    # Download Adjusted Closing Data for the last 5 years
    get_data = yf.download(sp500_components.loc[i, 'Symbol'], period='5y')['Adj Close']
    # Calculate daily returns
    get_returns = get_data.pct_change()
    # Calculate the mean of the daily returns and save it in the DataFrame
    sp500_components.loc[i, 'Mean_return'] = get_returns.mean()
    # Calculate the annualized return
    try:
        total_return = (get_data[-1]-get_data[0])/get_data[0]
        sp500_components.loc[i, 'Annualized_Return'] = (1+total_return)**(1/5)-1
    except:
        sp500_components.loc[i, 'Annualized_Return'] = np.nan
    # Calculate the Standard Deviation of returns    
    daily_std = get_returns.std()
    # Annualize the daily Standard Deviation
    sp500_components.loc[i, 'Annualized_Std'] = daily_std*np.sqrt(252)

sp500_components.to_csv('S&P_Database_Mean_Std_Return', header=True)
