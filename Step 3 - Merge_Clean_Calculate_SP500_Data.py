# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:50:17 2021

@author: LK
"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize S&P 500 (GSPC) Ticker as a market proxy

market_ticker = yf.Ticker('^GSPC')

# Read previously generated csv files and store them as DataFrame

sp500_components_mean_return = pd.read_csv(r"C:\Users\LK\Documents\Universität\Python\Portfolio-Project\S&P_Database_Mean_Std", index_col=0)
sp500_components_info = pd.read_csv(r"C:\Users\LK\Documents\Universität\Python\Portfolio-Project\S&P_Database_Info_Sustainability", index_col=0)

# Clean DataFrame

sp500_components_mean_return.drop(labels=['Ticker'], axis=1, inplace=True)

# Merge both DataFrames

sp500_components = pd.merge(sp500_components_info, sp500_components_mean_return, on="Symbol")

# Drop Rows with NaN

sp500_components.dropna(subset=['Beta'], how='any', inplace=True)
sp500_components.dropna(subset=['Annualized_Return'], how='any', inplace=True)
sp500_components.dropna(subset=['Mean_return'], how='any', inplace=True)
sp500_components.dropna(subset=['Gambling'], how='any', inplace=True)

# Reset Index

sp500_components.reset_index(drop=True, inplace=True)

# Calculate Sharpe Ratios

for i in np.arange(len(sp500_components)):
   sp500_components.loc[i, 'Sharpe'] = sp500_components.loc[i, 'Annualized_Return']/sp500_components.loc[i,'Annualized_Std']

# Download Data for S&P as an index

market_data = market_ticker.history(period="5y")['Close']

# Calculate Total Market Return 

total_market_return = (market_data[-1]-market_data[0])/market_data[0]

# Annualize Total Market Return

annualized_total_market_return = (1+total_market_return)**(1/5)-1

# Calculate Expected Return based on CAPM 

risk_free_rate = 0

for i in np.arange(len(sp500_components)):
    sp500_components.loc[i, 'Expected_Return'] = risk_free_rate + sp500_components.loc[i, 'Beta'] * (annualized_total_market_return-risk_free_rate)

sp500_components.to_csv('S&P_Database_Cleaned_and_Merged', header=True)











