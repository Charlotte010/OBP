# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:13:06 2024

@author: charl
"""
import pandas as pd

import os
os.chdir('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Simulation_code\char')

    
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
amount_of_runs = 10000
amount_of_simulations = 2



info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1, amount_of_simulations)
info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_2, amount_of_simulations)


    

    
 #-----------------------------------------------------------------------------------------------------------------------
 #Constraints
 
def c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available,info_handled_elderly_queue,waiting, max_expected_waiting_time):
    
    queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting)
    
    while queue_1_waiting_time > max_expected_waiting_time:
        amount_beds_available += 1
        info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available, amount_of_simulations)
        queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting)
        
    return queue_1_waiting_time, amount_beds_available



c1_queue1_wait, c1_queue1_beds  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1, 
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1) 

c1_queue2_wait, c1_queue2_beds  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_2, 
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2) 
                
   
    
 

#---------------------------------------------------------------------------------------------------------------------------
#Getting information

# Count how many have through_waiting_2 equal to 0 and 1

percentage_1 = 0
percentage_0 = 0
for i in info_handled_elderly_queue_2:
    
    count_through_0 = sum(1 for elderly in i if elderly.through_waiting_2 == 0)
    count_through_1 = sum(1 for elderly in i if elderly.through_waiting_2 == 1)
    total = count_through_0 + count_through_1
    
    percentage_1 += count_through_1 /total
    percentage_0 += count_through_0/ total

percentage_1 = percentage_1 / len(info_handled_elderly_queue_2)   
percentage_0 = percentage_0 / len(info_handled_elderly_queue_2) 


def compute_expected_waiting_time(info_handled_elderly_queue_1, waiting_queue):
    
    if waiting_queue == 'waiting_time':
        total_waiting_time = sum(elderly.waiting_time for elderly in info_handled_elderly_queue_1) 

    if  waiting_queue == 'waiting_time_in_list_3':
        
        total_waiting_time = sum(elderly.waiting_time_in_list_3 for elderly in info_handled_elderly_queue_1) 
        
        
    return total_waiting_time, len(info_handled_elderly_queue_1)


def compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, waiting_queue):
    total_expected_waiting_times = 0
    total_elderly_handled = 0
    
    for i in info_handled_elderly_queue_1:
        expected_waiting_times, elderly_handled = compute_expected_waiting_time(i, waiting_queue)
        
        total_expected_waiting_times +=expected_waiting_times
        total_elderly_handled += elderly_handled
        
    
    Excpected_waiting_times = total_expected_waiting_times / total_elderly_handled
    return Excpected_waiting_times



queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time")
queue_2_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3")

    

    
#TO DO 
# - Percentage of how often are all the beds occupied?
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting
# - make parameter of percentage how many days should wait























