# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:29:35 2024

@author: charl
"""

import os
os.chdir('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Simulation_code')

# main.py
from functions import *
import pandas as pd


table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')

care_level = "Low_Complex"
medical = "General_Practitioner"

# Example usage
list_elderly_info = getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical)

print(list_elderly_info)
