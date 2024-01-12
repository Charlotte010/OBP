# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:13:06 2024

@author: charl
"""
import pandas as pd

import os
os.chdir('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Simulation_code')

    
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
    

# main.py
from functions import *
import pandas as pd
from main_char_queue_1 import simulation_qeueue_1
from main_char_queue_2 import simulation_qeueue_2

amount_beds_available_1 = 5
amount_beds_available_2 = 100

amount_of_runs = 500
amount_of_simulations = 20


#plot_probabilities ("GRZ", info_handled_elderly_queue_2, table_probability)




def multiple_simulations(queue_simulation, amount_of_runs, amount_beds_available, amount_of_simulations):
    info_handled_elderly =[]
    for i in range(0,amount_of_simulations):
        
        info_handled_elderly.append(queue_simulation(amount_of_runs, amount_beds_available))

# Or using list comprehension
    return info_handled_elderly
    

info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1, amount_of_simulations)
info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_2, amount_of_simulations)


#TO DO 
# - Percentage of how often are all the beds occupied?
# - What is the percentage of people going from W2 to W3? 
# - 




















