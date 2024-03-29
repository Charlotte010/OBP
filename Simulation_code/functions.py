# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:08:43 2024

@author: charl
"""

# arrival_functions.py
import numpy as np
import pandas as pd
from .Class_Elderly import elderly

# data = {
#     "High_Complex": [0.578, 0.107, 0.198, 0.034, 0.023, 0.06],
#     "GRZ": [0.6, 0.107, 0.21, 0.0, 0.023, 0.06],
#     "Low_Complex": [0.7, 0.14, 0.1, 0.02, 0.02, 0.02],
#     "Respite_Care": [0.9, 0.05, 0.03, 0.01, 0.005, 0.005]
# }
#
# # Index (row labels) for the table
# index = ["Home", "Home_with_adjustments", "Long-term_care", "Geriatric_Rehabilitation", "Hospital_Care", "Death"]
#
# # Creating the DataFrame
# outflow_table = pd.DataFrame(data, index=index)
#
#
# # Data for the Arrival Rate table
# arrival_rate_data = {
#     "High_Complex": [1.34, 1.83, 0.94],
#     "GRZ": [0.0, 0.0, 0.54],
#     "Low_Complex": [1.34, 0.0, 0.0],
#     "Respite_Care": [0.57, 0.0, 0.0]
# }
#
# # Index (row labels) for the Arrival Rate table
# arrival_rate_index = ["General_Practitioner", "Emergency_Department", "Hospital"]
#
# # Creating the DataFrame for Arrival Rates
# arrival_rate_table = pd.DataFrame(arrival_rate_data, index=arrival_rate_index)
#
# # Data for the Service Rates table
# service_rate_data = {
#     "High_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
#     "GRZ": [31.1, 43.9, 47.8, 0.0, 22.9, 22.9],
#     "Low_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
#     "Respite_Care": [14.0, 43.9, 47.8, 29.8, 22.9, 22.9]
# }
#
# # Index (row labels) for the Service Rates table
# service_rate_index = ["Home", "Home_with_adjustments", "Long-term_care", "Geriatric_Rehabilitation",
#                       "Hospital_Care", "Death"]
#
# # Creating the DataFrame for Service Rates
# service_rate_table = pd.DataFrame(service_rate_data, index=service_rate_index)
#
# print(outflow_table)
# print(arrival_rate_table)
# print(service_rate_table)

def arrival_per_day(table, care_level, medical):
    arrival_rate = table.loc[medical, care_level]

    if arrival_rate > 0:
        arrivals_per_day = np.random.poisson(arrival_rate)
        return arrivals_per_day
    else:
        
        return 0

# probability_functions.py

def probability_goes_where(table, care_level, medical):
    probabilities = table[care_level]
    goes_where = np.random.choice(probabilities.index, p=probabilities)
    return goes_where


# service_time_functions.py

def service_time(table, care_level, goes_where):
    service_time = table.loc[goes_where, care_level]
    service_time = np.random.exponential(scale=service_time)
    return service_time



def getting_info_elderly(outflow_table, arrival_rate_table, service_rate_table, care_level, medical):
    
    goes_where = probability_goes_where(outflow_table, care_level, medical)
    service_time_elderly = service_time(service_rate_table, care_level, goes_where)
    
    list_elderly = [care_level, medical, service_time_elderly, goes_where]
    return list_elderly


def make_elderly_class(outflow_table, arrival_rate_table, service_rate_table, care_level, medical, binary):
    list_elderly_info = getting_info_elderly(outflow_table, arrival_rate_table, service_rate_table, care_level, medical)
    e1 = elderly(care_level, medical, list_elderly_info[2],list_elderly_info[3], binary)
    
    return e1



def multiple_simulations(queue_simulation, amount_of_runs, amount_beds_available, amount_of_simulations,
                         arrival_rate_table, outflow_table, service_rate_table):
    info_handled_elderly =[]
    for i in range(0,amount_of_simulations):
        
        info_handled_elderly.append(queue_simulation(amount_of_runs, amount_beds_available,
                                                     arrival_rate_table, outflow_table, service_rate_table))

# Or using list comprehension
    return info_handled_elderly
    


#-----------------------------------------------------------------------------------------------------------------
#Getting information

# Count how many have through_waiting_2 equal to 0 and 1
def percentage_through_2_3(info_handled_elderly_queue_2):
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
    
    return percentage_1, percentage_0

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





 #-----------------------------------------------------------------------------------------------------------------------
 #Constraints
 
def c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available,info_handled_elderly_queue,waiting, max_expected_waiting_time,amount_of_runs, amount_of_simulations,
                                    arrival_rate_table, outflow_table, service_rate_table):
    
    queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting)
    
    while queue_1_waiting_time > max_expected_waiting_time:
        amount_beds_available += 1
        info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available, amount_of_simulations)
        queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting)
        
    return queue_1_waiting_time, amount_beds_available







#CHECK IF WE GET THE SAME INFO WE EXPECTED-----------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd

def plot_probabilities(care_level, info_handled_elderly_queue_1_list,outflow_table):
    # Filter instances with care_level 'Low_Complex'
    low_complex_instances = [elderly_instance for elderly_instance in info_handled_elderly_queue_1_list if elderly_instance.care_level == care_level]
    
    # Get the next locations for 'Low_Complex' instances
    next_locations = [elderly_instance.goes_where for elderly_instance in low_complex_instances]
    # Count the occurrences of each next location
    location_counts = {location: next_locations.count(location) for location in set(next_locations)}
    
    # Calculate probabilities
    total_instances = len(low_complex_instances)
    location_probabilities_sim = {location: count / total_instances for location, count in location_counts.items()}
    
    # Create a DataFrame from the dictionary
    df_sim = pd.DataFrame.from_dict(location_probabilities_sim, orient='index', columns=['Simulated Probabilities'])
    
    low_complex_probabilities = outflow_table[care_level]
    
    merged_df = pd.merge(low_complex_probabilities, df_sim, left_index=True, right_index=True, how='left')
    
    
    fig, ax = plt.subplots()
    
    bar_width = 0.35
    locations_shifted = range(len(merged_df.index))
    
    ax.bar(locations_shifted, merged_df[care_level], width=bar_width, color='b', align='center', label=care_level)
    ax.bar([pos + bar_width for pos in locations_shifted], merged_df['Simulated Probabilities'], width=bar_width, color='g', align='center', alpha=0.5, label='Simulated Probabilities')
    
    ax.set_xlabel('Location')
    ax.set_ylabel('Probability')
    ax.set_title('Comparison of Low Complex and Simulated Probabilities')
    ax.set_xticks([pos + bar_width/2 for pos in locations_shifted])
    ax.set_xticklabels(merged_df.index,  rotation=90)
    
    ax.legend()
    
    plt.show()
    
    
    
    
    



