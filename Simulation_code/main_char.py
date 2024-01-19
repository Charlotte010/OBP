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
from functions_char import *
import pandas as pd
from main_char_queue_1 import simulation_qeueue_1
from main_char_queue_2 import simulation_qeueue_2

#parameters for queue 1
amount_beds_available_1 = 20 #low complex 
amount_beds_available_2 = 20 #Respite care 
percentage_1 = 50 #Parameters bedsharing


#parameters for queue 2
amount_beds_available_3 = 325 #High_complex
amount_beds_available_4 = 325 #GRZ
percentage_2 = 0 #Parameters bedsharing

#up to us
amount_of_runs = 1000
amount_of_simulations = 2


#parameters for Constraint 1 (C1)
max_expected_waiting_time_1 = 5
max_expected_waiting_time_2 = 20


#Decentralisation (C2)
list_amount_nurses = [40,10,4]
list_amount_beds = [45,20,35]
amount_beds_nurse_can_handle = 5



def compute_efficient_beds(list_amount_nurses,list_amount_beds, amount_beds_nurse_can_handle):
    amount_handled_beds = [x * amount_beds_nurse_can_handle for x in list_amount_nurses]

    efficient_beds = [min(x, y) for x, y in zip(amount_handled_beds, list_amount_beds)]
    efficient_beds = sum(efficient_beds)
    return efficient_beds

def distribution_beds (efficient_beds):
    
    
    
    return amount_beds_available_1, amount_beds_available_2, percentage_1


efficient_beds = compute_efficient_beds(list_amount_nurses,list_amount_beds, amount_beds_nurse_can_handle)    
    
    

info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
queue_1_waiting_time_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


queue_2_waiting_time_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")


#constraint 1 ----------------------------------------------------------------------------------------
# amount beds 1 is for low complex, is in this code the target bed to check
c1_queue1_wait_1, c1_queue1_beds_1  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Low_Complex', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 

# #amount fo Respite_Care
c1_queue1_wait_2, c1_queue1_beds_2  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_2,amount_beds_available_1,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Respite_Care', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 

# #amount fo High_complex
c1_queue2_wait_3, c1_queue2_beds_3  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_3, amount_beds_available_4,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "High_Complex" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 

#Amount for GRZ
c1_queue2_wait_4, c1_queue2_beds_4  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_4, amount_beds_available_3,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "GRZ" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 


    




#TO DO 
# - Percentage of how often are all the beds occupied?
# - CHANGE percentage shared beds just to a number of beds
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting for queue2
# - DONE (C1) - make parameter of percentage how many days should wait























