# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:43:49 2024

@author: charl
"""


def simulation_qeueue_2(amount_of_runs, beds_available_2, beds_available_3, shared_beds, 
                        table_probability, table_arrival_rates, table_E_service_rate):

      #list_elderly = [care_level, medical, service_time_elderly, goes_where]
    
    
    # main.py
    from functions_char import arrival_per_day,make_elderly_class, bed_shared
    import pandas as pd
        
     
    # table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
    # table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
    # table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
       
    
    list_care_queue2 = ["High_Complex", "GRZ"]
    list_medical_queue2 = ['General_Practitioner', 'Hospital', 'Emergency_Department']
    
    
    waiting_list_2 = [] #High_Complex
    waiting_list_3 = [] #High_Complex
    waiting_list_4 = [] #GRZ
    
    
    bed_queue_2 = [] #High_Complex
    bed_queue_3 = [] #GRZ
    bed_queue_shared = [] 
    
    handled_cases_queue_2 = []
    
    

    
    for i in range(0,amount_of_runs):  
        
         #Update the days in bed for all the elderly in the waiting list2
        for p in range(0,len(bed_queue_2)):
            bed_queue_2[p].increment_days_in_bed()
        
        for p in range(0,len(bed_queue_3)):
            bed_queue_3[p].increment_days_in_bed()   
            
        #Update the waiting time/service time for all the elderly in the waiting list3
        for p in range(0,len(waiting_list_3)):
            waiting_list_3[p].increment_days_in_bed()
           
            waiting_list_3[p].increment_waiting_time_in_list_3()
        
        #Update the waiting time/service time for all the elderly in the waiting list3
        for p in range(0,len(waiting_list_4)):
            waiting_list_4[p].increment_days_in_bed()
           
            waiting_list_4[p].increment_waiting_time_in_list_3()

        
        #Update the waiting time for all the elderly in the waiting list
        for p in range(0,len(waiting_list_2)):
            
            waiting_list_2[p].increment_waiting_time()
    
    
    
        
        #check if someone can be discharged and go out the queueing system
        #we fo the for loop like this because then we start from the end go from right to left. 
        for p in range(len(bed_queue_2) - 1, -1, -1):
            if bed_queue_2[p].days_in_bed >= bed_queue_2[p].service_time_elderly:
                
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_2.append(bed_queue_2.pop(p))  

        for p in range(len(bed_queue_3) - 1, -1, -1):
    
            if bed_queue_3[p].days_in_bed >= bed_queue_3[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_2.append(bed_queue_3.pop(p))  

        for p in range(len(bed_queue_shared) - 1, -1, -1):
    
            if bed_queue_shared[p].days_in_bed >= bed_queue_shared[p].service_time_elderly:
                # Remove the elderly instance from bed_queue_1 and add to handled_cases_queue_1
                handled_cases_queue_2.append(bed_queue_shared.pop(p))  
            
            
        for p in range(len(waiting_list_3) - 1, -1, -1):    
            if waiting_list_3[p].waiting_time_in_list_3 >= waiting_list_3[p].service_time_elderly:
                handled_cases_queue_2.append(waiting_list_3.pop(p)) 
            
            
        for p in range(len(waiting_list_4) - 1, -1, -1):    
            if waiting_list_4[p].waiting_time_in_list_3 >= waiting_list_4[p].service_time_elderly:
                handled_cases_queue_2.append(waiting_list_4.pop(p)) 
                  
            
            
        #Here we check for new arrivals and add them to the waiting list 2
        #BUT if they go through hospital Admission then to waitling list 3
        for care in list_care_queue2:
            
           
            for medical in list_medical_queue2:
                
                amount_arrive = arrival_per_day(table_arrival_rates, care, medical)  
                if amount_arrive >0:
                
                    if care == "High_Complex":
                        
                        for i in range(0,amount_arrive):
                            if medical == 'Hospital':
                                e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical, 0)
                                
                                waiting_list_3.append(e1)
                            else:
                                e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical, 1)
                                
                                waiting_list_2.append(e1)

                                
                    if care == "GRZ":
                            #print(medical) #SHOULD ALL BE HOSPITAL
                    
                            e1 = make_elderly_class(table_probability, table_arrival_rates, table_E_service_rate, care, medical, 0)

                            waiting_list_4.append(e1)

            
        #want to send a elderly from the waiting list 2 to the bed if there is space
        while len(bed_queue_2) < beds_available_2 and len(waiting_list_2)> 0:
            first_elderly = waiting_list_2.pop(0)
            bed_queue_2.append(first_elderly)
    
        #If there are still elderly left in waiting list 2, they should go to the Hospital
        #admission, so the elderly left in waiting list 2 will go to waiting list 3
        
        while len(bed_queue_2) >0 and len(waiting_list_2)> 0 :
            first_elderly = waiting_list_2.pop(0)
            waiting_list_3.append(first_elderly)
        
        #So now waitinglist 2 should be empty by or placing people in a bed_queue_2 or in waiting list 3. 
        #So now we have to check if there is a bed available still for someone in waiting list 3. 
        while len(bed_queue_2) < beds_available_2 and len(waiting_list_3)> 0 :
            first_elderly = waiting_list_3.pop(0)
            bed_queue_2.append(first_elderly)
        
        while len(bed_queue_3) < beds_available_3 and len(waiting_list_4)> 0 :
            first_elderly = waiting_list_4.pop(0)
            bed_queue_3.append(first_elderly)
            
        #now we need to look into if some can go to bed sharing
        
        # if shared_beds >0:
        #     while len(bed_queue_shared) < shared_beds and len(waiting_list_3)> 0:
        #         first_elderly = waiting_list_3.pop(0)
        #         first_elderly.set_shared_bed()
        #         bed_queue_shared.append(first_elderly) 
            
        #     while len(bed_queue_shared) < shared_beds and len(waiting_list_4)> 0:
        #         first_elderly = waiting_list_4.pop(0)
        #         first_elderly.set_shared_bed()
        #         bed_queue_shared.append(first_elderly) 
            
        if shared_beds >0:
           while len(bed_queue_shared) < shared_beds and (len(waiting_list_3)> 0 or  len(waiting_list_4)> 0) :
               
               if len(waiting_list_3)== 0 and len(waiting_list_4)> 0:
                   first_elderly = waiting_list_4.pop(0)
                   first_elderly.set_shared_bed()
                   bed_queue_shared.append(first_elderly) 
                   
               elif len(waiting_list_4)== 0 and len(waiting_list_3)> 0:
                   first_elderly = waiting_list_3.pop(0)
                   first_elderly.set_shared_bed()
                   bed_queue_shared.append(first_elderly) 
                   
               elif len(waiting_list_4) >0 and len(waiting_list_3)> 0:
                   if waiting_list_3[0].waiting_time_in_list_3 >= waiting_list_4[0].waiting_time_in_list_3:
                       first_elderly = waiting_list_3.pop(0)
                       first_elderly.set_shared_bed()
                       bed_queue_shared.append(first_elderly) 
                       
                   elif waiting_list_4[0].waiting_time_in_list_3 > waiting_list_3[0].waiting_time_in_list_3:
                       first_elderly = waiting_list_4.pop(0)
                       first_elderly.set_shared_bed()
                       bed_queue_shared.append(first_elderly) 
    
    handled_cases_queue_2 = handled_cases_queue_2[1000:]

    return handled_cases_queue_2
    
     
    
 
    
 

 