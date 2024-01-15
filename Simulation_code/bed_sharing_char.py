# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:52:44 2024

@author: charl
"""

import os
import pandas as pd
import math

os.chdir('C:\\Users\\charl\\OneDrive\\Documents\\VU vakken\\OBP\\Simulation_code')

    
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
    

# main.py
from functions import *
from main_char_queue_1 import simulation_qeueue_1
from main_char_queue_2 import simulation_qeueue_2

#parameters
amount_beds_available_1 = 50
amount_beds_available_2 = 165
bed_sharing_percentage = 10

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


#up to us
amount_of_runs = 1000


list_care_queue2 = ["High_Complex", "GRZ"]
list_medical_queue2 = ['General_Practitioner', 'Hospital', 'Emergency_Department']

list_care_queue1 = ["Low_Complex", "Respite_Care"]
list_medical_queue1 = ['General_Practitioner']


#queue 1
waiting_list_1 = []
bed_queue_1 = []
handled_cases_queue_1 = []


#queue 2
waiting_list_2 = []
waiting_list_3 = []

bed_queue_2 = []
handled_cases_queue_2 = []

#bed sharing
 
bed_queue_share = []
handled_Cases_shared = []

if bed_sharing_percentage > 0:
    amount_of_beds_shared, amount_beds_available_1, amount_beds_available_2 = bed_shared(bed_sharing_percentage, amount_beds_available_1, amount_beds_available_2  )

    
for i in range(0,amount_of_runs):  
    
     #Update the days in bed for all the elderly in the waiting list2
     #print(len(bed_queue_1))
    for p in range(0,len(bed_queue_2)):
        bed_queue_2[p].increment_days_in_bed()   
    

        #Update the waiting time for all the elderly in the waiting list
        #print(len(bed_queue_1))
    for p in range(0,len(bed_queue_1)):
        bed_queue_1[p].increment_days_in_bed()
            
    
    #Update the waiting time/service time for all the elderly in the waiting list3
    for p in range(0,len(waiting_list_3)):
        waiting_list_3[p].increment_days_in_bed()
       
        waiting_list_3[p].increment_waiting_time_in_list_3()
        #print(waiting_list_3[p].waiting_time_in_list_3)
    
    #Update the waiting time for all the elderly in the waiting list'2 
    for p in range(0,len(waiting_list_2)):
        
        waiting_list_2[p].increment_waiting_time()
    
    #Update the waiting time for all the elderly in the waiting list 1
    for p in range(0,len(waiting_list_1)):
            
        waiting_list_1[p].increment_waiting_time()
            
            

    
    #check if someone can be discharged and go out the queueing system
    #we fo the for loop like this because then we start from the end go from right to left. 
    for p in range(len(bed_queue_2) - 1, -1, -1):

        if bed_queue_2[p].days_in_bed >= bed_queue_2[p].service_time_elderly:
            # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
            handled_cases_queue_2.append(bed_queue_2.pop(p))  
        
    for p in range(len(waiting_list_3) - 1, -1, -1):    
        if waiting_list_3[p].waiting_time_in_list_3 >= waiting_list_3[p].service_time_elderly:
            handled_cases_queue_2.append(waiting_list_3.pop(p)) 
            
    #check if someone can be discharged and go out the queue1
    for p in range(len(bed_queue_1) - 1, -1, -1):
    
        if bed_queue_1[p].days_in_bed >= bed_queue_1[p].service_time_elderly:
            # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
            handled_cases_queue_1.append(bed_queue_1.pop(p))        
        
    for p in range(len(bed_queue_share) - 1, -1, -1):

        if bed_queue_share[p].days_in_bed >= bed_queue_share[p].service_time_elderly:
             # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
            handled_Cases_shared.append(bed_queue_share.pop(p))      
        
      
    #Here we check for new arrivals and add them to the waiting list 2
    #BUT if they go through hospital Admission then to waitling list 3 
    for care in list_care_queue2:
       
        for medical in list_medical_queue2:
            amount_arrive = arrival_per_day(table_arrival_rates, care, medical)  
            
                
            for i in range(0,amount_arrive):
                if medical == 'Hospital':
                    e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical, 0)
                    
                    waiting_list_3.append(e1)
                else:
                    e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical, 1)
                    
                    waiting_list_2.append(e1)

    #Here we check for new arrivals and add them to the waiting list  
    for care in list_care_queue1:
        for medical in list_medical_queue1:
            amount_arrive = arrival_per_day(table_arrival_rates, care, medical)    
            for i in range(0,amount_arrive):
                e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical,0)
                waiting_list_1.append(e1)
                
    
    
        
        
    #want to send a elderly from the waiting list 2 to the bed if there is space
    while len(bed_queue_2) < amount_beds_available_2 and len(waiting_list_2)> 0:
        first_elderly = waiting_list_2.pop(0)
        bed_queue_2.append(first_elderly)
        
    while len(bed_queue_share) < amount_of_beds_shared and len(waiting_list_2)> 0:
        first_elderly = waiting_list_2.pop(0)
        bed_queue_share.append(first_elderly)
        
        
    #If there are still elderly left in waiting list 2, they should go to the Hospital
    #admission, so the elderly left in waiting list 2 will go to waiting list 3
    while len(bed_queue_2) >0 and len(waiting_list_2)> 0 :
        first_elderly = waiting_list_2.pop(0)
        waiting_list_3.append(first_elderly)
    
    
    
    #So now waitinglist 2 should be empty by or placing people in a bed_queue_2 or in waiting list 3. 
    #So now we have to check if there is a bed available still for someone in waiting list 3. 
    while len(bed_queue_2) < amount_beds_available_2 and len(waiting_list_3)> 0 :
        first_elderly = waiting_list_3.pop(0)
        bed_queue_2.append(first_elderly)

    #want to send a elderly from the waiting list to the bed if there is space
    while len(bed_queue_1) < amount_beds_available_1 and len(waiting_list_1)> 0:
        first_elderly = waiting_list_1.pop(0)
        bed_queue_1.append(first_elderly)
        
        
        
        
        
        
        
        
        
        
    