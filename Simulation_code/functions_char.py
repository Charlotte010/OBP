# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:08:43 2024

@author: charl
"""

import numpy as np
from Class_Elderly_char import elderly


def arrival_per_day(table, care_level, medical):
    arrival_rate = table.loc[medical, care_level]

    if arrival_rate > 0:
        arrivals_per_day = np.random.poisson(arrival_rate)
        return arrivals_per_day
    else:
        
        return 0

#---To make elderly
def probability_goes_where(table, care_level, medical):
    probabilities = table[care_level]
    goes_where = np.random.choice(probabilities.index, p=probabilities)
    return goes_where



def service_time(table, care_level, goes_where):
    service_time = table.loc[goes_where, care_level]
    service_time = np.random.exponential(scale=service_time)
    return service_time



def getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical):
    
    goes_where = probability_goes_where(table_probability, care_level, medical)
    service_time_elderly = service_time(table_E_service_rate, care_level, goes_where)
    
    list_elderly = [care_level, medical, service_time_elderly, goes_where]
    return list_elderly


def make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical, binary):
    list_elderly_info = getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical)
    e1 = elderly(care_level, medical, list_elderly_info[2],list_elderly_info[3], binary )
    
    return e1

#-----------------

def multiple_simulations(queue_simulation, amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate):
    info_handled_elderly =[]
    for i in range(0,amount_of_simulations):
        
        info_handled_elderly.append(queue_simulation(amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage,
                                table_probability, table_arrival_rates, table_E_service_rate))

    return info_handled_elderly
    


#-----------------------------------------------------------------------------------------------------------------
#Getting information

# Count how many have through_waiting_2 equal to 0 and 1
def percentage_through_2_3(info_handled_elderly_queue_2):
    percentage_1 = 0
    percentage_0 = 0
    for i in info_handled_elderly_queue_2:
        high_complex_instances = [elderly_instance for elderly_instance in i if elderly_instance.care_level == "High_Complex"]

        count_through_0 = sum(1 for elderly in high_complex_instances if elderly.through_waiting_2 == 0)
        count_through_1 = sum(1 for elderly in high_complex_instances if elderly.through_waiting_2 == 1)
        total = count_through_0 + count_through_1
        
        percentage_1 += count_through_1 /total
        percentage_0 += count_through_0/ total
    
    percentage_1 = percentage_1 / len(info_handled_elderly_queue_2)   
    percentage_0 = percentage_0 / len(info_handled_elderly_queue_2) 
    
    return percentage_1, percentage_0

def compute_expected_waiting_time(info_handled_elderly_queue_1, waiting_queue, care_level):
    
    if waiting_queue == 'waiting_time':
        total_waiting_time = sum(elderly.waiting_time for elderly in info_handled_elderly_queue_1) 

    if  waiting_queue == 'waiting_time_in_list_3':
        
        total_waiting_time = sum(elderly.waiting_time_in_list_3 for elderly in info_handled_elderly_queue_1) 
        
        
    return total_waiting_time, len(info_handled_elderly_queue_1)


def compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, waiting_queue, care_level):
    total_expected_waiting_times = 0
    total_elderly_handled = 0
    
    for i in info_handled_elderly_queue_1:
        
        
        instances = [elderly_instance for elderly_instance in i if elderly_instance.care_level == care_level]

        expected_waiting_times, elderly_handled = compute_expected_waiting_time(instances, waiting_queue, care_level)
        
        total_expected_waiting_times +=expected_waiting_times
        total_elderly_handled += elderly_handled
        
    if total_elderly_handled>0:
        Excpected_waiting_times = total_expected_waiting_times / total_elderly_handled
    else:
        Excpected_waiting_times =0
    return Excpected_waiting_times







 #-----------------------------------------------------------------------------------------------------------------------
 #Constraints
 #bed 1 is the beds where we do the constraint on
def c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,info_handled_elderly_queue,waiting, 
                                    max_expected_waiting_time,amount_of_runs, amount_of_simulations, care_level ,percentage,
                                                            table_probability, table_arrival_rates, table_E_service_rate):
    
    queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
    
    while queue_1_waiting_time > max_expected_waiting_time:
        amount_beds_available_1 += 1
        
        info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2, percentage, amount_of_simulations,
                                table_probability, table_arrival_rates, table_E_service_rate)
        
        
        queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)
        
    return queue_1_waiting_time, amount_beds_available_1








def bed_shared(percentage, amount_beds_available_1, amount_beds_available_2  ):
    
    total_beds = amount_beds_available_1 + amount_beds_available_2
    bed_shared_total= (percentage/100) *  total_beds
    #bed_shared_total = math.floor(bed_shared_total)
    
    percentage_1 = amount_beds_available_1/ total_beds
    percentage_2 = amount_beds_available_2/ total_beds
    
    left_beds = total_beds - bed_shared_total
    amount_beds_available_1_new = round(percentage_1 * left_beds)
    amount_beds_available_2_new = round(percentage_2 * left_beds)
    bed_shared_total = round(bed_shared_total)
    
    return bed_shared_total, amount_beds_available_1_new, amount_beds_available_2_new









#CHECK IF WE GET THE SAME INFO WE EXPECTED-----------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd

def plot_probabilities(care_level, info_handled_elderly_queue_1_list,table_probability):
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
    
    low_complex_probabilities = table_probability[care_level]
    
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
    
    
    
    
    



