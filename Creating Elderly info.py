# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:25:18 2024

@author: charl
"""


import pandas as pd
import numpy as np



#Care level is High complex, low complex etc. (Represents the columns)
#Medical, is through which medical "department" does the patient goes through,
#So for example GP, Emergency departments etc. 



def arrival_per_day(table, care_level, medical):
    arrival_rate = table_arrival_rates.loc[medical, care_level]
    if arrival_rate== float:
        arrivals_per_day = np.random.poisson(arrival_rate)
       
        return arrivals_per_day
    else :
        return print("NOT POSSIBLE")

def probability_goes_where(table_probability, care_level, medical):
    
    #check if right value
    probabilities = table_probability[medical]
    selected_index = np.random.choice(len(probabilities), p=probabilities)
    goes_where = table_probability[selected_index]
    
    return goes_where

def service_time(table_E_service_rate,care_level, medical):
    
    arrival_rate = table_E_service_rate[care_level][medical]
    service_time = np.random.exponential(scale=1/arrival_rate)
    
    return service_time

    

def getting_info_elderly(table_probability,table_arrival_rates, table_E_service_rate, care_level ,medical):
    
    goes_where = probability_goes_where(table_probability, care_level, medical)
    service_time_elderly = service_time(table_E_service_rate, care_level, medical)
    list_elderly = [care_level ,medical, service_time_elderly, goes_where]
    
    return list_elderly


table_probability = pd.read_excel('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBp\\Service_Rates.xlsx',index_col='Unnamed: 0')


arrivale_rate_elderly  = arrival_per_day(table_arrival_rates, care_level, medical)

list_elderly_info =  getting_info_elderly(table_probability,table_arrival_rates, 
                                          table_E_service_rate, care_level ,medical)

HALLO =  "HALLO"

list_situation_1_care = ["Low_complex, Respite_care"]
list_situation_1_medical = ['General_practitioner']

















