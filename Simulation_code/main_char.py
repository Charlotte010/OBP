# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:29:35 2024

@author: charl
"""

import os
os.chdir('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Simulation_code')

  #list_elderly = [care_level, medical, service_time_elderly, goes_where]


# main.py
from functions import *
import pandas as pd


def arrival_per_day(table, care_level, medical):
    arrival_rate = table.loc[medical, care_level]

    if arrival_rate > 0:
        arrivals_per_day = np.random.poisson(arrival_rate)
        return arrivals_per_day
    else:
        
        return print("NOT POSSIBLE")
    
 
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
   

#TO DO NEXT IS LOOP TROUGH THE RIGHT POSSIBLE OPTIONS FOR QUEUE 1, AND QUEUE 2 
#care_level = "Low_Complex"
#medical = "General_Practitioner"

list_care_queue1 = ["Low_Complex", "Respite_Care"]
list_medical_queue1 = ['General_Practitioner']



waiting_list_1 = []


for i in range(0,300):    
    
    #Update the waiting time for all the elderly in the waiting list
    for p in range(0,len(waiting_list_1)):
        
        waiting_list_1[p].increment_waiting_time()
        
        
    #Here we check for new arrivals and add them to the waiting list  
    for care in list_care_queue1:
        print(care)
        for medical in list_medical_queue1:
            amount_arrive = arrival_per_day(table_arrival_rates, care, medical)
            print(amount_arrive)
    
            for i in range(0,amount_arrive):
                e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical)
                waiting_list_1.append(e1)
    

    
    
 
    
 
e2 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical)

