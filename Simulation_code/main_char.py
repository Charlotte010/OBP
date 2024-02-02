# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:13:06 2024

@author: charl
"""


import pandas as pd

import os
os.chdir('C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP\\Simulation_code')

    
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
    

# main.py
from .functions_char import *
import pandas as pd
from .main_char_queue_1 import simulation_qeueue_1
from .main_char_queue_2 import simulation_qeueue_2

#parameters for queue 1
amount_beds_available_1 = 0 #low complex 
amount_beds_available_2 = 0#Respite care 
percentage_1 = 100 #Parameters bedsharing


#parameters for queue 2
amount_beds_available_3 =0 #High_complex
amount_beds_available_4 = 0 #GRZ
percentage_2 = 200 #Parameters bedsharing

#up to us
amount_of_runs = 1500
amount_of_simulations =15


#parameters for Constraint 1 (C1)
max_expected_waiting_time_1 = 5
max_expected_waiting_time_2 = 5


#Decentralisation (C2)
amount_beds_nurse_can_handle = 5

list_locations_beds = [[8,8,8 ]] # first LC, RC, Shared
list_locations_nurses = [[5, 5,5]] # first LC, RC, Shared


#-------------------------------------------------------------------------------------------------------------------
#minimum amount of beds needed

# max_arrival_rates = []
# for column_name in table_arrival_rates.columns:
#     max_arrival_rates.append(table_arrival_rates[column_name].max())



#-------------------------------------------------------------------------------------------------------------
#Expected waiting time calculating



#--------------------------------------------------------------------------------------------------------------------




info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



queue_1_waiting_time_1, all_waiting_times_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")




queue_1_waiting_time_2, all_waiting_times_2  = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")





info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)


queue_2_waiting_time_3, all_waiting_times_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4, all_waiting_times_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")





#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time_1, all_waiting_times_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
queue_1_waiting_time_2, all_waiting_times_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


queue_2_waiting_time_3, all_waiting_times_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4, all_waiting_times_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")






#constraint 1 ----------------------------------------------------------------------------------------
# amount beds 1 is for low complex, is in this code the target bed to check


c1_queue1_wait_1, c1_queue1_beds_1  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Low_Complex', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 



# #amount fo Respite_Care
c1_queue1_wait_2, c1_queue1_beds_2  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Respite_Care', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 

# #amount fo High_complex
c1_queue2_wait_3, c1_queue2_beds_3  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_3, amount_beds_available_4,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "High_Complex" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 

#Amount for GRZ
c1_queue2_wait_4, c1_queue2_beds_4  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_3, amount_beds_available_4,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "GRZ" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 




#Constraint 2 centrali decentrali----------------------------------------------------------------------



#so efficient_beds is a list with the beds, so contains 3 integers all representing the new available beds
# in the order of LC, RC, shared beds These can you use for futher code by calling efficient_beds[0], efficient_beds[1], efficient_beds[2]
efficient_beds = efficient_beds_per_care_level(list_locations_beds, list_locations_nurses , amount_beds_nurse_can_handle)    
    
    




#-------------------------
#ROB
#- mogen we formules gebruiken, of simulation










