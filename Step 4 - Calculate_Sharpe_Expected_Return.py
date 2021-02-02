# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 21:56:39 2021

@author: LK
"""

import yfinance as yf
import pandas as pd
import numpy as np

# Read previously generated csv

sp500_components = pd.read_csv(r'C:/Users/LK/Documents/Universität/Python/Portfolio-Project/S&P_Database_Cleaned_and_Merged')

# Initialize S&P 500 (GSPC) Ticker as a market proxy

market_ticker = yf.Ticker('^GSPC')

# Drop columns

sp500_components.drop(['Unnamed: 0'], axis=1, inplace=True)

# Calculate Sharpe Ratios

for i in np.arange(len(sp500_components)):
   sp500_components.loc[i, 'Sharpe'] = sp500_components.loc[i, 'Annualized Return']/sp500_components.loc[i,'Annualized Std']

# Calculate Expected Return based on Mean Expectations of Analysts

for i in np.arange(len(sp500_components)):
    sp500_components.loc[i, 'Exp. Return (Target)'] = (sp500_components.loc[i, 'Mean Target']-sp500_components.loc[i, 'Last Price'])/sp500_components.loc[i, 'Last Price']

# Download Data for S&P as an index

market_data = market_ticker.history(period="5y")['Close']

# Calculate Total Market Return 

total_market_return = (market_data[-1]-market_data[0])/market_data[0]

# Annualize Total Market Return

annualized_total_market_return = (1+total_market_return)**(1/5)-1

# Calculate Expected Return based on CAPM 

risk_free_rate = 0

for i in np.arange(len(sp500_components)):
    sp500_components.loc[i, 'Exp. Return (CAPM)'] = risk_free_rate + sp500_components.loc[i, 'Beta'] * (annualized_total_market_return-risk_free_rate)

sp500_components.to_csv('S&P_Database_Final', header=True)