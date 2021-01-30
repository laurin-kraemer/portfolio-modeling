# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 17:17:16 2021

@author: LK
"""

import yfinance as yf
import numpy as np
import pandas as pd

# Get List of S&P 500 companies and save them in a Dataframe

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
data = table[0]
sp500_components = pd.DataFrame(data=data, columns=['Symbol'])


# Initialize Ticker objects

arange = np.arange(len(sp500_components))
for i in arange:
    sp500_components.loc[i, 'Ticker'] = yf.Ticker(sp500_components.loc[i, 'Symbol'])

# Get relevant data from Ticker.info and append it to the DataFrame

for i in arange:
    try:
        sp500_components.loc[i, 'Name'] = sp500_components.loc[i, 'Ticker'].info['shortName']
    except:
        sp500_components.loc[i, 'Name'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Market_Cap'] = sp500_components.loc[i, 'Ticker'].info['marketCap']
    except:
        sp500_components.loc[i, 'Market_Cap'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Two_Hundred_Day_Average'] = sp500_components.loc[i, 'Ticker'].info['twoHundredDayAverage']
    except:
        sp500_components.loc[i, 'Two_Hundred_Day_Average'] = np.nan    
        
for i in arange:
    try:
        sp500_components.loc[i, 'FiftyTwo_Week_Low'] = sp500_components.loc[i, 'Ticker'].info['fiftyTwoWeekLow']
    except:
        sp500_components.loc[i, 'FiftyTwo_Week_Low'] = np.nan          
        
for i in arange:
    try:
        sp500_components.loc[i, 'FiftyTwo_Week_High'] = sp500_components.loc[i, 'Ticker'].info['fiftyTwoWeekHigh']
    except:
        sp500_components.loc[i, 'FiftyTwo_Week_High'] = np.nan              
        

for i in arange:
    try:
        sp500_components.loc[i, 'Industry'] = sp500_components.loc[i, 'Ticker'].info['industry']
    except:
        sp500_components.loc[i, 'Industry'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Beta'] = sp500_components.loc[i, 'Ticker'].info['beta']
    except:
        sp500_components.loc[i, 'Beta'] = np.nan

for i in arange:
    try:
        sp500_components.loc[i, 'Forward_PE'] = sp500_components.loc[i, 'Ticker'].info['forwardPE']
    except:
        sp500_components.loc[i, 'Forward_PE'] = np.nan

for i in arange:
    try:
        sp500_components.loc[i, 'Price_to_Book'] = sp500_components.loc[i, 'Ticker'].info['priceToBook']  
    except:
        sp500_components.loc[i, 'Price_to_Book'] = np.nan      

for i in arange:
    try:
        sp500_components.loc[i, 'Dividend_Yield'] = sp500_components.loc[i, 'Ticker'].info['dividendYield']
    except:
        sp500_components.loc[i, 'Dividend_Yield'] = np.nan  
        
for i in arange:
    try:
        sp500_components.loc[i, 'Profit_Margins'] = sp500_components.loc[i, 'Ticker'].info['profitMargins']
    except:
        sp500_components.loc[i, 'Profit_Margins'] = np.nan

# Get relevant data from Ticker.sustainability and append it to the DataFrame

for i in arange:
    try:
        sp500_components.loc[i, 'controversialWeapons'] = sp500_components.loc[i, 'Ticker'].sustainability.loc[['controversialWeapons']].bool()
    except:
        sp500_components.loc[i, 'controversialWeapons'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Gambling'] = sp500_components.loc[i, 'Ticker'].sustainability.loc[['gambling']].bool()
    except:
        sp500_components.loc[i, 'Gambling'] = np.nan

for i in arange:
    try:
        sp500_components.loc[i, 'Alcoholic'] = sp500_components.loc[i, 'Ticker'].sustainability.loc[['alcoholic']].bool()
    except:
        sp500_components.loc[i, 'Alcoholic'] = np.nan

for i in arange:
    try:
        sp500_components.loc[i, 'Tobacco'] = sp500_components.loc[i, 'Ticker'].sustainability.loc[['tobacco']].bool()
    except:
        sp500_components.loc[i, 'Tobacco'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Animal Testing'] = sp500_components.loc[i, 'Ticker'].sustainability.loc[['animalTesting']].bool()
    except:
        sp500_components.loc[i, 'Animal Testing'] = np.nan        
        
        
for i in arange:
    try:
        sp500_components.loc[i, 'Social Score'] = sp500_components.loc[i, 'Ticker'].sustainability.loc['socialScore','Value']
    except:
        sp500_components.loc[i, 'Social Score'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'Governance Score'] = sp500_components.loc[i, 'Ticker'].sustainability.loc['governanceScore','Value']
    except:
        sp500_components.loc[i, 'Governance Score'] = np.nan

for i in arange:
    try:
        sp500_components.loc[i, 'Environmental Score'] = sp500_components.loc[i, 'Ticker'].sustainability.loc['environmentScore','Value']
    except:
        sp500_components.loc[i, 'Environmental Score'] = np.nan
        
for i in arange:
    try:
        sp500_components.loc[i, 'ESG Score'] = sp500_components.loc[i, 'Ticker'].sustainability.loc['totalEsg','Value']
    except:
        sp500_components.loc[i, 'ESG Score'] = np.nan        


sp500_components.to_csv('S&P_Database_Info_Sustainability', header=True)
    
    
    
    
    






