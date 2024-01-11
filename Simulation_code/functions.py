# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:08:43 2024

@author: charl
"""

# arrival_functions.py
import numpy as np
from Class_Elderly import elderly


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



def getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical):
    
    goes_where = probability_goes_where(table_probability, care_level, medical)
    service_time_elderly = service_time(table_E_service_rate, care_level, goes_where)
    
    list_elderly = [care_level, medical, service_time_elderly, goes_where]
    return list_elderly


def make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical):
    list_elderly_info = getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical)
    e1 = elderly(care_level, medical, list_elderly_info[2],list_elderly_info[3] )
    
    return e1