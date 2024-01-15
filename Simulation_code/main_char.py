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

#parameters
amount_beds_available_1 = 50
amount_beds_available_2 = 160

#parameters for Constraint 1 (C1)
max_expected_waiting_time_1 = 3
max_expected_waiting_time_2 = 5

#up to us
amount_of_runs = 1000
amount_of_simulations = 2



info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1, amount_of_simulations)
info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_2, amount_of_simulations)


#constraint 1 ----------------------------------------------------------------------------------------
c1_queue1_wait, c1_queue1_beds  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1, 
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations) 

c1_queue2_wait, c1_queue2_beds  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_2, 
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations) 
                
#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time")
queue_2_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3")

    

    




#TO DO 
# - Percentage of how often are all the beds occupied?
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting for queue2
# - DONE (C1) - make parameter of percentage how many days should wait























