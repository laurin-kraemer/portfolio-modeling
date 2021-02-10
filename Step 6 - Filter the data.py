# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:50:12 2021

@author: LK
"""

import pandas as pd
import numpy as np

sp500_data = pd.read_csv(r"C:/Users/LK/Documents/Universität/Python/Portfolio-Project/S&P_Database_Final")

# Welcome message for our Portfolio-Builiding Tool

print("Let's build a portfolio together!")
print("Answer the following questions to get recommendations for your individualized portfolio:")

# Ethical constraints: Weapons

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

# Ethical constraints: Gambling

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

# Ethical constraints: Tobacco

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

# Ethical constraints: Animal Testing

animal_testing_yes_no = input("Do you feel comfortable investing in companies that test their products on animals? (Yes/No) ")

while animal_testing_yes_no != 'Yes' and animal_testing_yes_no != 'No':
    animal_testing_yes_no = input("Please enter a valid input: (Yes/No) ")

if animal_testing_yes_no == 'No':
    # Do nothing
    None
else:
    # Filter out all the companies that have test their products on animals
    filter_array = sp500_data.loc[:, 'Animal Testing'] == False
    sp500_data = sp500_data[filter_array]

print(len(sp500_data))

# Find out importance of ESG for investor

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







    




