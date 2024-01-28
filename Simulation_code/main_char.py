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
amount_beds_available_1 = 65 #low complex 
amount_beds_available_2 = 20 #Respite care 
percentage_1 = 0 #Parameters bedsharing


#parameters for queue 2
amount_beds_available_3 = 100 #High_complex
amount_beds_available_4 = 21 #GRZ
percentage_2 = 100 #Parameters bedsharing

#up to us
amount_of_runs = 1000
amount_of_simulations =50


#parameters for Constraint 1 (C1)
max_expected_waiting_time_1 = 5
max_expected_waiting_time_2 = 5


#Decentralisation (C2)

amount_beds_nurse_can_handle = 5

list_locations_beds = [[10,5,2], [14,4,4]]  # first LC, RC, Shared
list_locations_nurses = [[2,3,0], [2,2,2]] # first LC, RC, Shared


#-------------------------------------------------------------------------------------------------------------------
#minimum amount of beds needed

# max_arrival_rates = []
# for column_name in table_arrival_rates.columns:
#     max_arrival_rates.append(table_arrival_rates[column_name].max())



service_times = table_probability * table_E_service_rate
column_sums = service_times.sum(axis=0).tolist()
service_rate = [1 / x for x in column_sums]


arrival_rates = table_arrival_rates.sum(axis=0).tolist()

rho = [lamb / u for u,lamb  in zip (service_rate, arrival_rates) ]

#high complex, GRZ, LC, RC
rho_we_want = 0.80
beds =    [rho / rho_we_want for rho  in rho ]


#--------------------------------------------------------------------------------------------------------------------




#so efficient_beds is a list with the beds, so contains 3 integers all representing the new available beds
# in the order of LC, RC, shared beds These can you use for futher code by calling efficient_beds[0], efficient_beds[1], efficient_beds[2]
efficient_beds = efficient_beds_per_care_level(list_locations_beds, list_locations_nurses , amount_beds_nurse_can_handle)    
    
    


info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)




info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time_1, all_waiting_times_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
queue_1_waiting_time_2, all_waiting_times_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


queue_2_waiting_time_3, all_waiting_times_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4, all_waiting_times_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")




# Count how many have through_waiting_2 equal to 0 and 1----------------------------------------------------
def percentage_through_2_3(info_handled_elderly_queue_2):
    percentage_1 = 0
    percentage_0 = 0
    for i in info_handled_elderly_queue_2:
        high_complex_instances = [elderly_instance for elderly_instance in i if (elderly_instance.medical == "General_Practitioner" or "Emergency_Department")]

        count_through_0 = sum(1 for elderly in high_complex_instances if elderly.through_waiting_2 == 0)
        count_through_1 = sum(1 for elderly in high_complex_instances if elderly.through_waiting_2 == 1)
        total = count_through_0 + count_through_1
        if total >0: 
            percentage_1 += count_through_1 /total
            percentage_0 += count_through_0/ total
            
    
    
    percentage_1 = percentage_1 / len(info_handled_elderly_queue_2)   
    percentage_0 = percentage_0 / len(info_handled_elderly_queue_2) 
    
    return percentage_1, percentage_0


percentage_through_3, percentage_not_through = percentage_through_2_3(info_handled_elderly_queue_2)


#constraint 1 ----------------------------------------------------------------------------------------
# amount beds 1 is for low complex, is in this code the target bed to check

def c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,info_handled_elderly_queue,waiting, 
                                    max_expected_waiting_time,amount_of_runs, amount_of_simulations, care_level ,percentage,
                                                            table_probability, table_arrival_rates, table_E_service_rate):
    
    if care_level == "Low_Complex" or care_level == "High_Complex":
        queue_1_waiting_time , j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
        if queue_1_waiting_time > max_expected_waiting_time:
            while queue_1_waiting_time > max_expected_waiting_time:
                amount_beds_available_1 += 1
                
                info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2, percentage, amount_of_simulations,
                                        table_probability, table_arrival_rates, table_E_service_rate)
                
                
                queue_1_waiting_time, j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
        
        elif queue_1_waiting_time < max_expected_waiting_time:
            while queue_1_waiting_time < max_expected_waiting_time:
                amount_beds_available_1 -= 1
            
                info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2, percentage, amount_of_simulations,
                                        table_probability, table_arrival_rates, table_E_service_rate)
                
                
                queue_1_waiting_time, j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
            
            
            amount_beds_available_1 += 1
            return queue_1_waiting_time, amount_beds_available_1
        
        
    if care_level == "Respite_Care" or care_level == "GRZ":
        queue_1_waiting_time , j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
        if queue_1_waiting_time > max_expected_waiting_time:
            while queue_1_waiting_time > max_expected_waiting_time:
                amount_beds_available_2 += 1
                
                info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2, percentage, amount_of_simulations,
                                        table_probability, table_arrival_rates, table_E_service_rate)
                
                
                queue_1_waiting_time, j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
        
        elif queue_1_waiting_time < max_expected_waiting_time:
            while queue_1_waiting_time < max_expected_waiting_time:

                amount_beds_available_2 -= 1
            
                info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2, percentage, amount_of_simulations,
                                        table_probability, table_arrival_rates, table_E_service_rate)
                
                
                queue_1_waiting_time, j = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
            
            
            amount_beds_available_2 += 1        
        
    
            return queue_1_waiting_time, amount_beds_available_2





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




#Constraint 2 centrali decentrali---




#TO DO 
# - Percentage of how often are all the beds occupied?
# - CHANGE percentage shared beds just to a number of beds
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting for queue2
# - DONE (C1) - make parameter of percentage how many days should wait


















