# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:43:49 2024

@author: charl
"""
import pandas as pd
from .functions import arrival_per_day, make_elderly_class

# data = {
#         "High_Complex": [0.578, 0.107, 0.198, 0.034, 0.023, 0.06],
#         "GRZ": [0.6, 0.107, 0.21, 0.0, 0.023, 0.06],
#         "Low_Complex": [0.7, 0.14, 0.1, 0.02, 0.02, 0.02],
#         "Respite_Care": [0.9, 0.05, 0.03, 0.01, 0.005, 0.005]
#     }
#
#     # Index (row labels) for the table
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
#       "High_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
#       "GRZ": [31.1, 43.9, 47.8, 0.0, 22.9, 22.9],
#       "Low_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
#       "Respite_Care": [14.0, 43.9, 47.8, 29.8, 22.9, 22.9]
# }
#
# # Index (row labels) for the Service Rates table
# service_rate_index = ["Home", "Home_with_adjustments", "Long-term_care", "Geriatric_Rehabilitation",
#                       "Hospital_Care", "Death"]
#
# # Creating the DataFrame for Service Rates
# service_rate_table = pd.DataFrame(service_rate_data, index=service_rate_index)

def simulation_qeueue_2(amount_of_runs, amount_beds_available_2, arrival_rate, outflow, service_rate):

      #list_elderly = [care_level, medical, service_time_elderly, goes_where]
    
    
    # main.py
    # from .functions import arrival_per_day,make_elderly_class

     
    # table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
    # table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
    # table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')

    list_care_queue2 = ["High_Complex", "GRZ"]
    list_medical_queue2 = ['General_Practitioner', 'Hospital', 'Emergency_Department']
    
    
    
    waiting_list_2 = []
    waiting_list_3 = []
    
    bed_queue_2 = []
    handled_cases_queue_2 = []
    
    
    #Parameters 
    #amount_beds_available_2 = 127
    
    # SIMPLE QUEUE
    for i in range(0,amount_of_runs):  
        
         #Update the days in bed for all the elderly in the waiting list2
         #print(len(bed_queue_1))
        for p in range(0,len(bed_queue_2)):
            bed_queue_2[p].increment_days_in_bed()
            
        #Update the waiting time/service time for all the elderly in the waiting list3
        for p in range(0,len(waiting_list_3)):
            waiting_list_3[p].increment_days_in_bed()
           
            waiting_list_3[p].increment_waiting_time_in_list_3()
            #print(waiting_list_3[p].waiting_time_in_list_3)
        
        #Update the waiting time for all the elderly in the waiting list
        for p in range(0,len(waiting_list_2)):
            
            waiting_list_2[p].increment_waiting_time()
    
        
        #check if someone can be discharged and go out the queueing system
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_2) - 1, -1, -1):
    
            if bed_queue_2[p].days_in_bed >= bed_queue_2[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_2.append(bed_queue_2.pop(p))  
            
        for p in range(len(waiting_list_3) - 1, -1, -1):    
            if waiting_list_3[p].waiting_time_in_list_3 >= waiting_list_3[p].service_time_elderly:
                handled_cases_queue_2.append(waiting_list_3.pop(p)) 
         
            
            
        #Here we check for new arrivals and add them to the waiting list 2
        #BUT if they go through hospital Admission then to waitling list 3 (STILL NEED TO ADD)
        for care in list_care_queue2:
           
            for medical in list_medical_queue2:
                amount_arrive = arrival_per_day(arrival_rate, care, medical)
                
                    
                for i in range(0,amount_arrive):
                    if medical == 'Hospital':
                        e1 = make_elderly_class(outflow, arrival_rate, service_rate, care, medical, 0)
                        
                        waiting_list_3.append(e1)
                    else:
                        e1 = make_elderly_class(outflow, arrival_rate, service_rate, care, medical, 1)
                        
                        waiting_list_2.append(e1)
                        
            
        #want to send a elderly from the waiting list 2 to the bed if there is space
        while len(bed_queue_2) < amount_beds_available_2 and len(waiting_list_2)> 0:
            first_elderly = waiting_list_2.pop(0)
            bed_queue_2.append(first_elderly)
    
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
        
        
    return handled_cases_queue_2
    
     
    
 
    
 

 