# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:29:35 2024

@author: charl
"""



def simulation_qeueue_1(amount_of_runs,amount_beds_available_1,amount_beds_available_2,  percentage):
    #from functions import *
    import pandas as pd
    from functions_char import arrival_per_day,make_elderly_class, bed_shared

    
    
    list_care_queue1 = ["Low_Complex", "Respite_Care"]
    list_medical_queue1 = ['General_Practitioner']
    

    
    table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
    table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
    table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
    
    

    shared_beds, beds_available_1, beds_available_2 = bed_shared(percentage, amount_beds_available_1, amount_beds_available_2  )

    waiting_list_1 = [] #low complex
    waiting_list_2 = [] # Respite care
    bed_queue_1 = [] 
    bed_queue_2 = []
    bed_queue_shared = []

    
    handled_cases_queue_1 = []
    
    for i in range(0,amount_of_runs): 
        
        
        #check if someone can be discharged and go out the beds/queue
        
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_1) - 1, -1, -1):
    
            if bed_queue_1[p].days_in_bed >= bed_queue_1[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_1.append(bed_queue_1.pop(p)) 
        
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_2) - 1, -1, -1):
    
            if bed_queue_2[p].days_in_bed >= bed_queue_2[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_1.append(bed_queue_2.pop(p))  
                
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_shared) - 1, -1, -1):
    
            if bed_queue_shared[p].days_in_bed >= bed_queue_shared[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_1.append(bed_queue_shared.pop(p))                 
                
        
    
        #Update the waiting time for all the elderly in the waiting list
        for p in range(0,len(waiting_list_1)):
            
            waiting_list_1[p].increment_waiting_time()
            
       #Update the waiting time for all the elderly in the waiting list
        for p in range(0,len(waiting_list_2)):
           
            waiting_list_2[p].increment_waiting_time()




        #Update the service time for all the elderly in the waiting list
        for p in range(0,len(bed_queue_1)):
            bed_queue_1[p].increment_days_in_bed()      
        
        #Update the service time for all the elderly in the waiting list
        for p in range(0,len(bed_queue_2)):
            bed_queue_2[p].increment_days_in_bed()  
        
        #Update the service time for all the elderly in the waiting list
        for p in range(0,len(bed_queue_shared)):
            bed_queue_shared[p].increment_days_in_bed()  
          
            
          
            
          
        #Here we check for new arrivals and add them to the waiting list  
        for care in list_care_queue1:
            
            for medical in list_medical_queue1:
                
                
                amount_arrive = arrival_per_day(table_arrival_rates, care, medical) 
                if care == 'Low_Complex':
                
                    for i in range(0,amount_arrive):
                        e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical,0)
                        waiting_list_1.append(e1)
                
                if care == "Respite_Care":
                    for i in range(0,amount_arrive):
                        e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical,0)
                        waiting_list_2.append(e1)        
        
        
            
            
        #want to send a elderly from the waiting list to the bed if there is space
        while len(bed_queue_1) < beds_available_1 and len(waiting_list_1)> 0:
            first_elderly = waiting_list_1.pop(0)
            bed_queue_1.append(first_elderly)

            
        #want to send a elderly from the waiting list to the bed if there is space
        while len(bed_queue_2) < beds_available_2 and len(waiting_list_2)> 0:
            first_elderly = waiting_list_2.pop(0)
            bed_queue_2.append(first_elderly)
            
            
        # Now the situation when beds are shared, Only now waiting list gets
        #priority over waiting list 2
        if shared_beds >0:
            while len(bed_queue_shared) < shared_beds and len(waiting_list_1)> 0:
                first_elderly = waiting_list_1.pop(0)
                first_elderly.set_shared_bed()
                bed_queue_shared.append(first_elderly) 
            
            while len(bed_queue_shared) < shared_beds and len(waiting_list_2)> 0:
                first_elderly = waiting_list_2.pop(0)
                first_elderly.set_shared_bed()
                bed_queue_shared.append(first_elderly) 
    
    
    return handled_cases_queue_1

 
    
 
    
 

 
    
    
    
 

