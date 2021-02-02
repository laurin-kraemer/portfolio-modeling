# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:50:17 2021

@author: LK
"""
import yfinance as yf
import pandas as pd

# Initialize S&P 500 (GSPC) Ticker as a market proxy

market_ticker = yf.Ticker('^GSPC')

# Read previously generated csv files and store them as DataFrame

sp500_components_mean_return = pd.read_csv(r"C:\Users\LK\Documents\Universität\Python\Portfolio-Project\S&P_Database_Mean_Std", index_col=0)
sp500_components_info = pd.read_csv(r"C:\Users\LK\Documents\Universität\Python\Portfolio-Project\S&P_Database_Info_Sustainability", index_col=0)

# Read barchart data

sp500_components_barchart_data = pd.read_csv(r'C:/Users/LK/Documents/Universität/Python/Portfolio-Project/sp-500-index-02-01-2021 (1).csv')

# Merge both sp500_components_mean_return with sp500_components_info 

sp500_components_merged = pd.merge(sp500_components_info, sp500_components_mean_return, on="Symbol")

# Merge newly generated DataFrame with Barchart data

sp500_components = sp500_components_merged.merge(right=sp500_components_barchart_data, on='Symbol', how='inner')

# Clean DataFrame

sp500_components.drop(labels=['Dividend_Yield', 'Beta_x', 'Mean_return', 'Ticker_y', 'Two_Hundred_Day_Average'], axis=1, inplace=True)

# Rename columns

sp500_components.rename(columns={'Name_x': 'Name'}, inplace=True)
sp500_components.rename(columns={'Ticker_x': 'Ticker'}, inplace=True)
sp500_components.rename(columns={'Market_Cap': 'Market Cap'}, inplace=True)
sp500_components.rename(columns={'FiftyTwo_Week_Low': '52 Week Low'}, inplace=True)
sp500_components.rename(columns={'FiftyTwo_Week_High': '52 Week High'}, inplace=True)
sp500_components.rename(columns={'Forward_PE': 'Forward PE'}, inplace=True)
sp500_components.rename(columns={'Price_to_Book': 'Price/Book'}, inplace=True)
sp500_components.rename(columns={'Profit_Margins': 'Profit Margins'}, inplace=True)
sp500_components.rename(columns={'controversialWeapons': 'Weapons'}, inplace=True)
sp500_components.rename(columns={'Annualized_Std': 'Annualized Std'}, inplace=True)
sp500_components.rename(columns={'Last': 'Last Price'}, inplace=True)
sp500_components.rename(columns={'Expected_Return': 'Exp. Return (CAPM)'}, inplace=True)
sp500_components.rename(columns={'Beta_y': 'Beta'}, inplace=True)
sp500_components.rename(columns={'Annualized_Return': 'Annualized Return'}, inplace=True)

# Drop Rows with NaN

sp500_components.dropna(subset=['Beta'], how='any', inplace=True)
sp500_components.dropna(subset=['Annualized Return'], how='any', inplace=True)
sp500_components.dropna(subset=['Gambling'], how='any', inplace=True)
sp500_components.dropna(subset=['Annualized Std'], how='any', inplace=True)

# Reset Index

sp500_components.reset_index(drop=True, inplace=True)

sp500_components.to_csv('S&P_Database_Cleaned_and_Merged', header=True)











