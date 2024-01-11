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
    
 
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
   

#care_level = "Low_Complex"
#medical = "General_Practitioner"

list_care_queue1 = ["Low_Complex", "Respite_Care"]
list_medical_queue1 = ['General_Practitioner']



waiting_list_1 = []
bed_queue_1 = []
handled_cases_queue_1 = []

#Parameters 
amount_beds_available = 50

# SIMPLE QUEUE
for i in range(0,300):    
    
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
            amount_arrive = arrival_per_day(table_arrival_rates, care, medical)    
            for i in range(0,amount_arrive):
                e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical)
                waiting_list_1.append(e1)
                
    
    
    #Update the waiting time for all the elderly in the waiting list
    #print(len(bed_queue_1))
    for p in range(0,len(bed_queue_1)):
        bed_queue_1[p].increment_days_in_bed()
        
        
    #want to send a elderly from the waiting list to the bed if there is space
    while len(bed_queue_1) < amount_beds_available and len(waiting_list_1)> 0:
        first_elderly = waiting_list_1.pop(0)
        bed_queue_1.append(first_elderly)




 
    
 
    
 

 
    
    
    
 

