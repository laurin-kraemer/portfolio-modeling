# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:52:25 2021

@author: LK
"""

import yfinance as yf
import pandas as pd
import numpy as np

# Read previously generated csv

sp500_components = pd.read_csv(r"C:/Users/LK/Documents/Universität/Python/Portfolio-Project/S&P_Database_Cleaned_and_Merged")

# Create List of Sp500 Symbols that can be used later for the columns of the Correlation Matrix

symbol_list = sp500_components.loc[:, 'Symbol'].to_list()

# Create empty DataFrame where Price Data can be stored

price_data = pd.DataFrame()

# Download Price Data for every ticker

for i in np.arange(len(symbol_list)):
    price_data.loc[:, i] = yf.download(sp500_components.loc[i, 'Symbol'], period='5y')['Adj Close']
 
# Assign the right column names   
 
price_data.columns = [symbol_list]

# Calculate returns

returns_data = price_data.pct_change()

cov_matrix = returns_data.cov()
cor_matrix = returns_data.corr()

cor_matrix.to_csv("Cov_Matrix_SP500")
cor_matrix.to_csv("Cor_Matrix_SP500")


