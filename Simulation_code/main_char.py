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
amount_beds_available_1 = 55 #low complex 
amount_beds_available_2 = 12 #Respite care 
percentage_1 = 0 #Parameters bedsharing


#parameters for queue 2
amount_beds_available_3 = 172 #High_complex
amount_beds_available_4 = 23 #GRZ
percentage_2 = 0 #Parameters bedsharing

#up to us
amount_of_runs = 1500
amount_of_simulations =15


# #parameters for Constraint 1 (C1)
# max_expected_waiting_time_1 = 5
# max_expected_waiting_time_2 = 5


# #Decentralisation (C2)
# amount_beds_nurse_can_handle = 5

# list_locations_beds = [[10,5,2], [14,4,4]]  # first LC, RC, Shared
# list_locations_nurses = [[2,3,0], [2,2,2]] # first LC, RC, Shared


#-------------------------------------------------------------------------------------------------------------------
#minimum amount of beds needed

# max_arrival_rates = []
# for column_name in table_arrival_rates.columns:
#     max_arrival_rates.append(table_arrival_rates[column_name].max())


mu_table= table_E_service_rate.copy()

for column in table_E_service_rate.columns:
    mu_table[column] = 1 / table_E_service_rate[column]
    
service_times = table_probability * mu_table
column_sums = service_times.sum(axis=0).tolist()


arrival_rates = table_arrival_rates.sum(axis=0).tolist()

rho = [lamb / u for u,lamb  in zip (column_sums, arrival_rates) ]

#high complex, GRZ, LC, RC
rho_we_want = 0.80
beds =    [rho / rho_we_want for rho  in rho ]


#-------------------------------------------------------------------------------------------------------------
#Expected waiting time calculating

def compute_p0(lambda_arrival, mu_service, num_servers):
    alp = lambda_arrival/mu_service
    rho = alp / (num_servers)
    # Calculate the traffic intensity factor
    a = sum([(alp) ** i / np.math.factorial(i) for i in range(0,num_servers-1)])
    b = (alp) ** num_servers / np.math.factorial(num_servers) * (1/(1-rho))

    p0 = (a + b)**-1
    
    return p0

def compute_Csa(lambda_arrival, mu_service, num_servers):
    rho = lambda_arrival / (num_servers * mu_service)
    a = lambda_arrival/mu_service
    
    # Calculate p0 using the previously defined function
    p0 = compute_p0(lambda_arrival, mu_service, num_servers)
    
    Csa = (1/(1-rho)) * (a**(num_servers)/np.math.factorial(num_servers) ) * p0
    
    return Csa



def compute_expected_waiting_time(lambda_arrival, mu_service, num_servers):
    
    # Calculate C(s, a) using the previously defined function
    Cs_a = compute_Csa(lambda_arrival, mu_service, num_servers)
    
    # Calculate E[W]
    expected_waiting_time = Cs_a / ((num_servers * mu_service) - lambda_arrival)
    
    return expected_waiting_time

E_W = compute_expected_waiting_time(arrival_rates[3], column_sums[3], 12)

#--------------------------------------------------------------------------------------------------------------------




info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



queue_1_waiting_time_1, all_waiting_times_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")




queue_1_waiting_time_2, all_waiting_times_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


import numpy as np
from scipy import stats
alpha = 0.05
z_critical = stats.norm.ppf(1 - alpha/2)

# Calculate mean and standard deviation from simulation
mean_simulated = np.mean(all_waiting_times_2)
std_dev_simulated = np.std(all_waiting_times_2)
margin_of_error2 = 1.96 * (std_dev_simulated / np.sqrt(len(all_waiting_times_2 )))




# Check if the expected waiting time from the function falls within the confidence interval
if confidence_interval[0] <= E_W <= confidence_interval[1]:
    print("The simulation results are consistent with the expected waiting time from the function.")
else:
    print("The simulation results are not consistent with the expected waiting time from the function.")



info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)




#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time_1, all_waiting_times_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
queue_1_waiting_time_2, all_waiting_times_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


queue_2_waiting_time_3, all_waiting_times_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4, all_waiting_times_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")




# Count how many have through_waiting_2 equal to 0 and 1----------------------------------------------------


percentage_through_3, percentage_not_through = percentage_through_2_3(info_handled_elderly_queue_2)




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
    
    


#TO DO 
# - Percentage of how often are all the beds occupied?
# - CHANGE percentage shared beds just to a number of beds
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting for queue2
# - DONE (C1) - make parameter of percentage how many days should wait


















