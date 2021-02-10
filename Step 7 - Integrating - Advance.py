# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 17:13:28 2021

@author: LK
@author: fabianschweinzer
"""

""" 
This Portfolio Optimizer Tool has to built-in functions.
The first function enables the optimization of an already existing portfolios based on current weights.
The second function is the creation of an optimized portfolio based on individual preferences.
"""

import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import yahoo_fin as yf
from pandas_datareader import data
from pypfopt import EfficientFrontier
from pypfopt import expected_returns, objective_functions
from pypfopt import CLA, plotting
from pypfopt import DiscreteAllocation
from datetime import datetime

## Welcome message for our Portfolio-Builiding Tool

print("Welcome to the Portfolio-Optimizer!")

## Importing a database of all the Stocks in the S&P
sp500_data = pd.read_csv('/Users/fabianschweinzer/Desktop/Hult International Business School/MFIN/Python/Group Project Group 3/portfolio-modeling-main/S&P_Database_Final')

## Check if User wants to optimize current porfolio or built a new one

print("Do you want to optimize an already existing portfolio (Option 1) or create a new one based on your individual preferences (Option 2)?")
optimize_or_built = input("Please enter A for Option 1 or B for Option 2")

while optimize_or_built != 'A' and optimize_or_built != 'B':
    optimize_or_built = input("Please enter a valid input")

if optimize_or_built == 'A':
    print('Please answer the following questions so we can optimize your portfolio')
    
    ##Start finding out information about the user's existing portfolio
       
    print('Please enter the Symbol followed by the shares you own')
    
    shares = pd.DataFrame()
    
    shares.loc[0, 'Stock'] = input('Stock Symbol')
    shares.loc[0, 'Shares'] = input('Number of Shares')
    
    ticker_list = sp500_data['Symbol'].tolist()

    ## Create a dataframe with ticker symbols and corresponding weights

    shares = pd.DataFrame()

    amount_shares = int(input("How many stocks do you have in your portfolio? "))

    i = 0
    while i < amount_shares:
        shares.loc[i, 'Symbol'] = input('Stock Symbol ' + str(i+1) + ': ')
        if shares.loc[i, 'Symbol'] in ticker_list:
            shares.loc[i, 'Shares'] = int(input('Number of Shares: '))
            i = i+1
        else:
            print("Please enter a valid out of S&P 500: ")

    database = pd.merge(left=sp500_data, right=shares, on='Symbol')
    database = database.drop('Unnamed: 0', axis=1)
    
    ## Fabians Magic
    
    database.set_index('Symbol', inplace=True)

    #extract expected return based on mean target return

    mu_target = database.iloc[:,-2]

    #initiate Cov Matrix 

    cov_matrix = pd.read_csv('/Users/fabianschweinzer/Desktop/Hult International Business School/MFIN/Python/Group Project Group 3/portfolio-modeling-main/Cov_Matrix_SP500')

    cov_matrix.set_index('Unnamed: 0', inplace = True)

    #initiate Cov Matrix 

    cov_matrix = pd.read_csv('Covariance Matrix')
    cov_matrix.set_index('Unnamed: 0', inplace = True)
    
    '''
    Start using pyopft in order to optimize Portfolio according to certain constraints
    Starting optimizer by defining mu and sigma 
    Calculate expected returns and sample covariance
    We already calculated mu and sigma in a previos step, so we can use these variables
    '''


    #calculate the EfficientFrontier using calculated mu, sigma
    ef = EfficientFrontier(mu_target, cov_matrix, weight_bounds=(0.0,0.2))
    ef.add_objective(objective_functions.L2_reg, gamma=1)
    target_volatility = 0.6
    #put in conditional arguments regarding the investors risk tolerance
    risk_tolerance = input("How do you want to optimize your portfolio? (Max Sharpe / Efficient Risk / Min Variance) ")

    while risk_tolerance != 'Max Sharpe' and risk_tolerance != 'Efficient Risk' and risk_tolerance != 'Min Variance':
        risk_tolerance = input("Please enter a valid input: (Max Sharpe / Efficient Risk / Min Variance) ")
    if risk_tolerance == 'Min Variance':
        weights = ef.min_volatility()
    elif risk_tolerance == 'Max Sharpe':
        weights = ef.max_sharpe()
    else:
        weights = ef.efficient_risk(target_volatility)

    #clean weights for a better visualization
    clean_weights = ef.clean_weights()
    ef.portfolio_performance(verbose = True)

    ##visualize the efficient frontier line
    #there is an issue here, if I want to run it, I will get a timeout
    #cla= CLA(mu_capm_sliced, cov_matrix)
    #cla.min_volatility()
    #cla.portfolio_performance(verbose=True)

    #there is some issue here regarding the cla return (probably to many requests a time)
    #ax = plotting.plot_efficient_frontier(cla, show_assets=True, show_fig=True )


    #step 2, as we can't specifiy exactly 25 stocks in the first round, we need to optimize again
    #we subset the outcome of the first optimization to the 25 stocks with the highest weights
    #reduce the size to 25 stocks in order to go to the next round of optimization
    df = pd.DataFrame.from_dict(data=clean_weights, orient='index')
    df.columns = ['Weight']
    df_filter = df['Weight'] > 0
    df_1 = df[df_filter].sort_values(by='Weight', ascending=False)
    df_1 = df_1.head(25)


    #slice the database to get only the 25 stocks and perform a second round of optimization
    #subseting the expected return
    mu_target_25 = mu_target[mu_target.index.isin(df_1.index)]

    #subsetting the cov matrix is more worrysome
    #I used a transpose technique to do the subsetting on both axis
    cov_matrix_25 = cov_matrix[cov_matrix.index.isin(df_1.index)]
    cov_matrix_25 = cov_matrix_25.T
    cov_matrix_25 = cov_matrix_25[cov_matrix_25.index.isin(df_1.index)]

    #Effficient Frontier optimization for the top25 stocks
    #we insert minimum weight limit, so every stocks gets a minimum weight of 1%
    #we also include a maximum weight limit, so to make sure there is not too much importance on one particular stock

    ef_25 = EfficientFrontier(mu_target_25, cov_matrix_25, weight_bounds=(0.01, 0.2))
    if risk_tolerance == 'Min Variance':
       weights_25 = ef_25.min_volatility()
    elif risk_tolerance == 'Efficient Risk':
        weights_25 = ef_25.max_sharpe()
    else:
        weights_25 = ef_25.efficient_risk(target_volatility)

    #clean weights and and print the performance indicators
    clean_weights_25 = ef_25.clean_weights()
    ef_25.portfolio_performance(verbose = True)

    print(clean_weights_25)

    '''
    From this stage on we have the cleaned weights so we can go ahead and visualize the outcomes
    '''

    #create piechart 
    piechart = pd.Series(clean_weights_25).plot.pie(figsize=(10,10))
    plt.show(piechart)

    #create barchart
    barchart = pd.Series(clean_weights_25).sort_values(ascending=True).plot.barh(figsize=(10,6))
    plt.show(barchart)

    #covariance heatmap
    plotting.plot_covariance(cov_matrix_25, plot_correlation = True)

    #create the Efficient frontier line and visualize it

    cla_25 = CLA(mu_target_25, cov_matrix_25)
    if risk_tolerance == 'Min Variance':
       cla_25.min_volatility()
    elif risk_tolerance == 'Efficient Risk':
        cla_25.max_sharpe()
    else:
       cla_25.efficient_risk(target_volatility)

    cla_25.portfolio_performance(verbose=True)

    #plot the efficient frontier line
    ax_25 = plotting.plot_efficient_frontier(cla_25, show_assets=False, show_fig=False )


    ####plot with ef function
    #risk_range = np.linspace(0.1, 0.4, 100)
    #ax_ef = plotting.plot_efficient_frontier(ef_25, ef_param='risk', ef_param_range=risk_range, show_assets=True, show_fig=True)

    #initialize Discrete Allocation to get a full picture what you could buy with a given amount
    

    tickers = pd.DataFrame.from_dict(data=clean_weights_25, orient='index')
    tickers_list = tickers.index.to_list()

    funds = 10000

    da = data.DataReader(tickers_list, data_source='yahoo', start=datetime(2021,1,28), end=datetime.today())['Adj Close']

    latest_price = da.iloc[-1,:]

    alloc = DiscreteAllocation(clean_weights_25,latest_prices=latest_price, total_portfolio_value=funds)
    allocation, leftover = alloc.lp_portfolio()
    print(allocation)
    print(leftover)

    pie_alloc = pd.Series(allocation).plot.pie(figsize=(10,10))
    plt.show(pie_alloc)  
    
       
else:
    print("Answer the following questions so we can select the right stocks for you")

    ## Ethical constraints: Weapons

    weapon_yes_no = input("Do you feel comfortable investing in companies that make their money with weapons? (Yes/No) ")

    while weapon_yes_no != 'Yes' and weapon_yes_no != 'No':
        weapon_yes_no = input("Please enter a valid input: (Yes/No) ")

    if weapon_yes_no == 'Yes':
        # Do nothing
        None
    else:
        # Filter out all the companies that have something to do with weapons
        filter_array = sp500_data.loc[:, 'Weapons'] == False
        sp500_data = sp500_data[filter_array]

    print(len(sp500_data))

    ## Ethical constraints: Gambling

    gambling_yes_no = input("Do you feel comfortable investing in companies that operate in the gambling sector? (Yes/No) ")

    while gambling_yes_no != 'Yes' and gambling_yes_no != 'No':
        gambling_yes_no = input("Please enter a valid input: (Yes/No) ")

    if gambling_yes_no == 'Yes':
        # Do nothing
        None
    else:
        # Filter out all the companies that have something to do with gambling
        filter_array = sp500_data.loc[:, 'Gambling'] == False
        sp500_data = sp500_data[filter_array]

    print(len(sp500_data))

    ## Ethical constraints: Tobacco

    tobacco_yes_no = input("Do you feel comfortable investing in companies that sell tobacco-products? (Yes/No) ")

    while tobacco_yes_no != 'Yes' and tobacco_yes_no != 'No':
        tobacco_yes_no = input("Please enter a valid input: (Yes/No) ")

    if tobacco_yes_no == 'Yes':
        # Do nothing
        None
    else:
        # Filter out all the companies that have something to do with tobacco
        filter_array = sp500_data.loc[:, 'Tobacco'] == False
        sp500_data = sp500_data[filter_array]

    print(len(sp500_data))

    ## Ethical constraints: Animal Testing

    animal_testing_yes_no = input("Do you feel comfortable investing in companies that test their products on animals? (Yes/No) ")

    while animal_testing_yes_no != 'Yes' and animal_testing_yes_no != 'No':
        animal_testing_yes_no = input("Please enter a valid input: (Yes/No) ")

    if animal_testing_yes_no == 'Yes':
        # Do nothing
        None
    else:
        # Filter out all the companies that have test their products on animals
        filter_array = sp500_data.loc[:, 'Animal Testing'] == False
        sp500_data = sp500_data[filter_array]

    print(len(sp500_data))

    ## Find out importance of ESG for investor

    esg_importance = input("How important is the ESG-criteria for you as investor? (Low/Medium/High) ")

    # Find out 25th, 50th and 75th percentile

    sp500_esg_25th_percentile = np.percentile(sp500_data.loc[:, "ESG Score"], 25)
    sp500_esg_50th_percentile = np.percentile(sp500_data.loc[:, "ESG Score"], 50)


    while esg_importance != 'Low' and esg_importance != 'Medium' and esg_importance != 'High':
        esg_importance = input("Please enter a valid input: (Low/Medium/High) ")

    if esg_importance == 'Low':
        # Do nothing
        None
    elif esg_importance == 'Medium':
        filter_array = sp500_data.loc[:, "ESG Score"] > sp500_esg_25th_percentile
        sp500_data = sp500_data[filter_array]
    else:
        filter_array = sp500_data.loc[:, "Annualized Std"] > sp500_esg_50th_percentile
        sp500_data = sp500_data[filter_array]
        
    """ 
    The output is a filtered list that can be used an an input for the Optimization    
    """
    
    
    # Assign filtered list to database
    database = sp500_data
    database.set_index('Symbol', inplace=True)

    #extract expected return based on mean target return

    mu_target = database.iloc[:,-2]

    #initiate Cov Matrix 

    cov_matrix = pd.read_csv('/Users/fabianschweinzer/Desktop/Hult International Business School/MFIN/Python/Group Project Group 3/portfolio-modeling-main/Cov_Matrix_SP500')

    cov_matrix.set_index('Unnamed: 0', inplace = True)

    #initiate Cov Matrix 

    cov_matrix = pd.read_csv('Covariance Matrix')
    cov_matrix.set_index('Unnamed: 0', inplace = True)
    
    '''
    Start using pyopft in order to optimize Portfolio according to certain constraints
    Starting optimizer by defining mu and sigma 
    Calculate expected returns and sample covariance
    We already calculated mu and sigma in a previos step, so we can use these variables
    '''


    #calculate the EfficientFrontier using calculated mu, sigma
    ef = EfficientFrontier(mu_target, cov_matrix, weight_bounds=(0.0,0.2))
    ef.add_objective(objective_functions.L2_reg, gamma=1)
    target_volatility = 0.6
    #put in conditional arguments regarding the investors risk tolerance
    risk_tolerance = input("How do you want to optimize your portfolio? (Max Sharpe / Efficient Risk / Min Variance) ")

    while risk_tolerance != 'Max Sharpe' and risk_tolerance != 'Efficient Risk' and risk_tolerance != 'Min Variance':
        risk_tolerance = input("Please enter a valid input: (Max Sharpe / Efficient Risk / Min Variance) ")
    if risk_tolerance == 'Min Variance':
        weights = ef.min_volatility()
    elif risk_tolerance == 'Max Sharpe':
        weights = ef.max_sharpe()
    else:
        weights = ef.efficient_risk(target_volatility)

    #clean weights for a better visualization
    clean_weights = ef.clean_weights()
    ef.portfolio_performance(verbose = True)

    ##visualize the efficient frontier line
    #there is an issue here, if I want to run it, I will get a timeout
    #cla= CLA(mu_capm_sliced, cov_matrix)
    #cla.min_volatility()
    #cla.portfolio_performance(verbose=True)

    #there is some issue here regarding the cla return (probably to many requests a time)
    #ax = plotting.plot_efficient_frontier(cla, show_assets=True, show_fig=True )


    #step 2, as we can't specifiy exactly 25 stocks in the first round, we need to optimize again
    #we subset the outcome of the first optimization to the 25 stocks with the highest weights
    #reduce the size to 25 stocks in order to go to the next round of optimization
    df = pd.DataFrame.from_dict(data=clean_weights, orient='index')
    df.columns = ['Weight']
    df_filter = df['Weight'] > 0
    df_1 = df[df_filter].sort_values(by='Weight', ascending=False)
    df_1 = df_1.head(25)


    #slice the database to get only the 25 stocks and perform a second round of optimization
    #subseting the expected return
    mu_target_25 = mu_target[mu_target.index.isin(df_1.index)]

    #subsetting the cov matrix is more worrysome
    #I used a transpose technique to do the subsetting on both axis
    cov_matrix_25 = cov_matrix[cov_matrix.index.isin(df_1.index)]
    cov_matrix_25 = cov_matrix_25.T
    cov_matrix_25 = cov_matrix_25[cov_matrix_25.index.isin(df_1.index)]

    #Effficient Frontier optimization for the top25 stocks
    #we insert minimum weight limit, so every stocks gets a minimum weight of 1%
    #we also include a maximum weight limit, so to make sure there is not too much importance on one particular stock

    ef_25 = EfficientFrontier(mu_target_25, cov_matrix_25, weight_bounds=(0.01, 0.2))
    if risk_tolerance == 'Min Variance':
       weights_25 = ef_25.min_volatility()
    elif risk_tolerance == 'Efficient Risk':
        weights_25 = ef_25.max_sharpe()
    else:
        weights_25 = ef_25.efficient_risk(target_volatility)

    #clean weights and and print the performance indicators
    clean_weights_25 = ef_25.clean_weights()
    ef_25.portfolio_performance(verbose = True)

    print(clean_weights_25)

    '''
    From this stage on we have the cleaned weights so we can go ahead and visualize the outcomes
    '''

    #create piechart 
    piechart = pd.Series(clean_weights_25).plot.pie(figsize=(10,10))
    plt.show(piechart)

    #create barchart
    barchart = pd.Series(clean_weights_25).sort_values(ascending=True).plot.barh(figsize=(10,6))
    plt.show(barchart)

    #covariance heatmap
    plotting.plot_covariance(cov_matrix_25, plot_correlation = True)

    #create the Efficient frontier line and visualize it

    cla_25 = CLA(mu_target_25, cov_matrix_25)
    if risk_tolerance == 'Min Variance':
       cla_25.min_volatility()
    elif risk_tolerance == 'Efficient Risk':
        cla_25.max_sharpe()
    else:
       cla_25.efficient_risk(target_volatility)

    cla_25.portfolio_performance(verbose=True)

    #plot the efficient frontier line
    ax_25 = plotting.plot_efficient_frontier(cla_25, show_assets=False, show_fig=False )


    ####plot with ef function
    #risk_range = np.linspace(0.1, 0.4, 100)
    #ax_ef = plotting.plot_efficient_frontier(ef_25, ef_param='risk', ef_param_range=risk_range, show_assets=True, show_fig=True)

    #initialize Discrete Allocation to get a full picture what you could buy with a given amount
    

    tickers = pd.DataFrame.from_dict(data=clean_weights_25, orient='index')
    tickers_list = tickers.index.to_list()

    funds = 10000

    da = data.DataReader(tickers_list, data_source='yahoo', start=datetime(2021,1,28), end=datetime.today())['Adj Close']

    latest_price = da.iloc[-1,:]

    alloc = DiscreteAllocation(clean_weights_25,latest_prices=latest_price, total_portfolio_value=funds)
    allocation, leftover = alloc.lp_portfolio()
    print(allocation)
    print(leftover)

    pie_alloc = pd.Series(allocation).plot.pie(figsize=(10,10))
    plt.show(pie_alloc)


