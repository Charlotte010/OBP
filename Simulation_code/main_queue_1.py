# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:29:35 2024

@author: charl
"""
import os
import sys

import pandas as pd
# os.chdir('C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP\\Simulation_code')
# sys.path.append('C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP\\Simulation_code')
#
# table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
# print(table_probability)

import pandas as pd
from .functions import arrival_per_day, make_elderly_class

# table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
# print(table_probability)
# table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
# table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')

#####input
# High_Complex_Home = 0.578
# High_Complex_Home_with_adjustments = 0.107
# High_Complex_Long_term_care = 0.198
# High_Complex_Geriatric_Rehabilitation = 0.034
# High_Complex_Hospital_Care = 0.023
# High_Complex_Death = 0.06
#
# GRZ_Home = 0.6
# GRZ_Home_with_adjustments= 0.107
# GRZ_Long_term_care= 0.21
# GRZ_Geriatric_Rehabilitation=0.0
# GRZ_Hospital_Care= 0.023
# GRZ_Death = 0.06
#
# Low_Complex_Home = 0.7
# Low_Complex_Home_with_adjustments = 0.14
# Low_Complex_Long_term_care = 0.1
# Low_Complex_Geriatric_Rehabilitation = 0.02
# Low_Complex_Hospital_Care =0.02
# Low_Complex_Death = 0.02
#
# Respite_Care_Home = 0.9
# Respite_Care_Home_with_adjustments = 0.05
# Respite_Care_Long-term_care = 0.03
# Respite_Care_Geriatric_Rehabilitation = 0.01
# Respite_Care_Hospital_Care = 0.005
# Respite_Care_Death = 0.005
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

def simulation_qeueue_1(amount_of_runs, amount_beds_available, arrival_rate, outflow, service_rate):
    #from functions import *

    list_care_queue1 = ["Low_Complex", "Respite_Care"]
    list_medical_queue1 = ['General_Practitioner']

    waiting_list_1 = []
    bed_queue_1 = []
    handled_cases_queue_1 = []
    
    for i in range(0,amount_of_runs): 
        
        
        #check if someone can be discharged and go out the queue
        
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_1) - 1, -1, -1):
    
            if bed_queue_1[p].days_in_bed >= bed_queue_1[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_1.append(bed_queue_1.pop(p))        
            
            
            
        #Update the waiting time for all the elderly in the waiting list
        for p in range(0,len(waiting_list_1)):
            
            waiting_list_1[p].increment_waiting_time()
            
            
        #Here we check for new arrivals and add them to the waiting list  
        for care in list_care_queue1:
            for medical in list_medical_queue1:
                amount_arrive = arrival_per_day(arrival_rate, care, medical)
                for i in range(0,amount_arrive):
                    e1 = make_elderly_class(outflow, arrival_rate, service_rate, care, medical,0)
                    waiting_list_1.append(e1)
                    
        
        
        #Update the waiting time for all the elderly in the waiting list
        #print(len(bed_queue_1))
        for p in range(0,len(bed_queue_1)):
            bed_queue_1[p].increment_days_in_bed()
            
            
        #want to send a elderly from the waiting list to the bed if there is space
        while len(bed_queue_1) < amount_beds_available and len(waiting_list_1)> 0:
            first_elderly = waiting_list_1.pop(0)
            bed_queue_1.append(first_elderly)
    
    
    return handled_cases_queue_1
