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

amount_beds_available_1 = 20
amount_beds_available_2 = 100

amount_of_runs = 1000
amount_of_simulations = 20



info_handled_elderly_queue_1 = simulation_qeueue_1(amount_of_runs,amount_beds_available_1)
info_handled_elderly_queue_2 = simulation_qeueue_2(amount_of_runs,amount_beds_available_2)

#plot_probabilities ("GRZ", info_handled_elderly_queue_2, table_probability)







import matplotlib.pyplot as plt

# Function to run the simulation for a given amount of beds
def run_simulation(amount_beds):
    info_handled_elderly_queue = simulation_qeueue_1(amount_of_runs, amount_beds)
    
    # Calculate the total waiting time
    total_waiting_time = sum(elderly.waiting_time for elderly in info_handled_elderly_queue)
    
    # Calculate the number of elderly individuals
    num_elderly = len(info_handled_elderly_queue)
    
    # Calculate the expected waiting time
    expected_waiting_time = total_waiting_time / num_elderly if num_elderly > 0 else 0
    
    return expected_waiting_time

# Set the range of beds (10 to 200 with a step of 1)
beds_range = range(10, 130)

# Run the simulation for each amount of beds
expected_waiting_times = [run_simulation(amount_beds) for amount_beds in beds_range]

# Plot the results
plt.plot(beds_range, expected_waiting_times, linestyle='-', color='b')
plt.xlabel('Amount of Beds')
plt.ylabel('Expected Waiting Time')
plt.title('Expected Waiting Time vs. Amount of Beds, for queue 1')
plt.grid(True)
plt.show()





















