# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:13:06 2024

@author: charl
"""
import pandas as pd
import matplotlib as plt

import os
os.chdir('C:\\Users\\p.giannakakos\\Downloads\\OBP\\Simulation_code')

    
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
    

# main.py
from functions_char import *
import pandas as pd
from main_char_queue_1 import simulation_qeueue_1
from main_char_queue_2 import simulation_qeueue_2

#parameters for queue 1
amount_beds_available_1 = 20 #low complex 
amount_beds_available_2 = 20 #Respite care 
percentage_1 = 50 #Parameters bedsharing


#parameters for queue 2
amount_beds_available_3 = 20 #High_complex
amount_beds_available_4 = 20 #GRZ
percentage_2 = 50 #Parameters bedsharing

#parameters for Constraint 1 (C1)
max_expected_waiting_time_1 = 50
max_expected_waiting_time_2 = 50

#up to us
amount_of_runs =2000
amount_of_simulations = 5

    
info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)



info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                        table_probability, table_arrival_rates, table_E_service_rate)


    
#getting information ------------------------------------------------------------------------------------

queue_1_waiting_time_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
queue_1_waiting_time_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")


queue_2_waiting_time_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
queue_2_waiting_time_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")

'''
#CODE FOR SIMULATION TEST

R=[500,1000,1500,2000,2500]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
for r in R:
    amount_of_runs = r
    #First queue
    L=list(range(45,55,1))
    M=list(range(12,22,1))
    waiting_times_low_complex=[]
    waiting_times_respite_care=[]
    for i in range(len(L)):
        amount_beds_available_2 = M[i]
        percentage_1 = 0 #Parameters bedsharing
        amount_beds_available_1= L[i]
        info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                                table_probability, table_arrival_rates, table_E_service_rate)
        queue_1_waiting_time_1,h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
        queue_1_waiting_time_2,g = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")
        waiting_times_low_complex.append(queue_1_waiting_time_1)
        waiting_times_respite_care.append(queue_1_waiting_time_2)
        

    # Plot on the first subplot
    ax1.plot(L, waiting_times_low_complex, label=f'Runs={amount_of_runs}')

    # Plot on the second subplot
    ax2.plot(M, waiting_times_respite_care, label=f'Runs={amount_of_runs}')

# Customize first subplot
ax1.set_xlabel('Number of Available Beds',fontsize=16)
ax1.set_ylabel('Expected Waiting Time (In Days)',fontsize=16)
ax1.set_title('Low Complex Cases',fontsize=18)
ax1.legend()

# Customize second subplot
ax2.set_xlabel('Number of Available Beds',fontsize=16)
ax2.set_ylabel('Expected Waiting Time (In Days)',fontsize=16)
ax2.set_title('Respite Care Cases',fontsize=18)
ax2.legend()

# Adjust layout to prevent clipping
plt.tight_layout()

# Show the combined plot
plt.show()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
for r in R:
    amount_of_runs = r
    #Second queue
    L=list(range(140,152))
    M=list(range(9,21))
    waiting_times_high_complex=[]
    waiting_times_G_R=[]
    for i in range(len(L)) :
        amount_beds_available_3= L[i]
        percentage_2 = 0 #Parameters bedsharing
        amount_beds_available_4= M[i]
        info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
                            table_probability, table_arrival_rates, table_E_service_rate)
        queue_2_waiting_time_3,h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
        queue_2_waiting_time_4,g = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")
        waiting_times_high_complex.append(queue_2_waiting_time_3)
        waiting_times_G_R.append(queue_2_waiting_time_4)
        
    # Plot on the first subplot
    ax1.plot(L, waiting_times_high_complex, label=f'Runs={amount_of_runs}')

    # Plot on the second subplot
    ax2.plot(M, waiting_times_G_R, label=f'Runs={amount_of_runs}')

# Customize first subplot
ax1.set_xlabel('Number of Available Beds',fontsize=16)
ax1.set_ylabel('Expected Waiting Time (In Days)',fontsize=16)
ax1.set_title('High Complex Cases',fontsize=18)
ax1.legend()

# Customize second subplot
ax2.set_xlabel('Number of Available Beds',fontsize=16)
ax2.set_ylabel('Expected Waiting Time (In Days)',fontsize=16)
ax2.set_title('GRZ Care Cases',fontsize=18)
ax2.legend()

# Adjust layout to prevent clipping
plt.tight_layout()

# Show the combined plot
plt.show()

'''

#Sensitivity analysis without Bed-sharing
#First queue
L=list(range(10,17,1))
M=list(range(5,12,1))
waiting_times_low_complex=[]
waiting_times_respite_care=[]
for i in range(len(L)):
    amount_beds_available_2 = M[i]
    percentage_1 = 0 #Parameters bedsharing
    amount_beds_available_1= L[i]
    info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                            table_probability, table_arrival_rates, table_E_service_rate)
    queue_1_waiting_time_1,h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
    queue_1_waiting_time_2,g = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")
    print(round(queue_1_waiting_time_1,2),'is the expected waiting time for Low complex cases with',L[i],'available beds')
    print(round(queue_1_waiting_time_2,2),'is the expected waiting time for Respite care cases with',M[i],'available beds') 
#     waiting_times_low_complex.append(queue_1_waiting_time_1)
#     waiting_times_respite_care.append(queue_1_waiting_time_2)
    
#     # Perform statistical calculations to obtain confidence interval
#     confidence_interval = 1.99  # Z-score for a 95% confidence interval
#     standard_deviation1 = np.std(h )
#     margin_of_error1 = confidence_interval * (standard_deviation1 / np.sqrt(len(h )))
#     standard_deviation2 = np.std(g )
#     margin_of_error2 = confidence_interval * (standard_deviation2 / np.sqrt(len(g )))
#     # Plotting
    
# plt.plot(L, waiting_times_low_complex, label='Low Complex Cases')
# plt.fill_between(L, waiting_times_low_complex - margin_of_error1,  waiting_times_low_complex + margin_of_error1, color='green', alpha=0.1, label='95% Confidence Interval')
# plt.xlabel('Number of Available Beds')
# plt.ylabel('Expected Waiting Time (In Days)')
# plt.title('E(W) for Different Numbers of Available Beds')
# plt.legend()
# plt.show()


# plt.plot(M, waiting_times_respite_care, label='Respite Care Cases')
# plt.fill_between(M, waiting_times_respite_care - margin_of_error2,  waiting_times_respite_care + margin_of_error2, color='green', alpha=0.1, label='95% Confidence Interval')
# plt.xlabel('Number of Available Beds',fontsize=14)
# plt.ylabel('Expected Waiting Time (In Days)',fontsize=14)
# plt.title('E(Wq) for Different Numbers of Available Beds',fontsize=16)
# plt.legend()
# plt.show()


# #Second queue
# L=list(range(140,152))
# M=list(range(9,21))
# waiting_times_high_complex=[]
# waiting_times_G_R=[]
# for i in range(len(L)) :
#     amount_beds_available_3= L[i]
#     percentage_2 = 0 #Parameters bedsharing
#     amount_beds_available_4= M[i]
#     info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
#                         table_probability, table_arrival_rates, table_E_service_rate)
#     queue_2_waiting_time_3,h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
#     queue_2_waiting_time_4,g = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")
#     waiting_times_high_complex.append(queue_2_waiting_time_3)
#     waiting_times_G_R.append(queue_2_waiting_time_4)
    
#     # Perform statistical calculations to obtain confidence interval
#     confidence_interval = 1.99  # Z-score for a 95% confidence interval
#     standard_deviation1 = np.std(h )
#     margin_of_error1 = confidence_interval * (standard_deviation1 / np.sqrt(len(h )))
#     standard_deviation2 = np.std(g )
#     margin_of_error2 = confidence_interval * (standard_deviation2 / np.sqrt(len(g )))
#     print(round(queue_2_waiting_time_3,2),'is the waiting time for High complex cases with',L[i],'available beds')
#     print(round(queue_2_waiting_time_4,2),'is the waiting time for Geriatric Rehabilitation cases with',M[i],'available beds') 

# plt.plot(L, waiting_times_high_complex, label='High Complex Cases')
# plt.fill_between(L, waiting_times_high_complex - margin_of_error1,  waiting_times_high_complex + margin_of_error1, color='green', alpha=0.1, label='95% Confidence Interval')
# plt.xlabel('Number of Available Beds',fontsize=14)
# plt.ylabel('Expected Waiting Time',fontsize=14)
# plt.title('E(Wq) for Different Numbers of Available Beds',fontsize=16)
# plt.legend()
# plt.show()


# plt.plot(M, waiting_times_G_R, label='Geriatric Rehabilitation')
# plt.fill_between(M, waiting_times_G_R - margin_of_error2,  waiting_times_G_R + margin_of_error2, color='green', alpha=0.1, label='95% Confidence Interval')
# plt.xlabel('Number of Available Beds')
# plt.ylabel('Expected Waiting Time')
# plt.title('E(Wq) for Different Numbers of Available Beds')
# plt.legend()
# plt.show()




#Sensitivity analysis with Bed-sharing

final_y1 =[]
final_x1 = []
final_y2 =[]
final_x2 = []

for j in list(range(2,5,1)):
    y_values_low_complex = []
    y_values_respite_care = []
    x1 = []
    x2 = []
    L=list(range(10,17,1))
    M=list(range(5,17,1))
    percentage_1 = j #Parameters bedsharing
    for i in range(len(L)) :
        amount_beds_available_2 = M[i]
        amount_beds_available_1= L[i]
        
        info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1,amount_of_runs, amount_beds_available_1,amount_beds_available_2,  percentage_1, amount_of_simulations,
                                table_probability, table_arrival_rates, table_E_service_rate)
        queue_1_waiting_time_1 ,h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Low_Complex")
        queue_1_waiting_time_2 , g= compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time", "Respite_Care")
        print(queue_1_waiting_time_1,'is the waiting time for Low complex cases with',L[i],'available beds and',j,'% shared beds')
        print(queue_1_waiting_time_2,'is the waiting time for Respite care cases with',M[i],'available beds and',j,'% shared beds')    
#         y_values_low_complex.append(queue_1_waiting_time_1)
#         y_values_respite_care.append(queue_1_waiting_time_2)
#         x1.append(L[i])
#         x2.append(M[i])
        
#     final_y1.append(y_values_low_complex)
#     final_x1.append(x1)
#     final_y2.append(y_values_respite_care)
#     final_x2.append(x2)
    
     
# plt.figure(figsize=(10, 6))   
# for i in range(len(final_x1)):
#     plt.plot(final_x1[i], final_y1[i],  label=f'Low Complex for {(1+i)*2} shared beds' )    


# plt.title('E(Wq) for Different Numbers of Available Beds')
# plt.xlabel('Available Beds')
# plt.ylabel('Expected Waiting Time')
# plt.legend()
# plt.show()


# plt.figure(figsize=(10, 6))   
# for i in range(len(final_x2)):
#     plt.plot(final_x2[i], final_y2[i],  label=f'Respite Care for {(1+i)*2} shared beds' )
    

# plt.title('E(Wq) for Different Numbers of Available Beds')
# plt.xlabel('Available Beds')
# plt.ylabel('Expected Waiting Time')
# plt.legend()
# plt.show()
  
    

# final_y1 =[]
# final_x1 = []
# final_y2 =[]
# final_x2 = []

# for j in list(range(5,20,5)): 
#     print(j)
#     percentage_2 = j #Parameters bedsharing
#     L=list(range(144,153,1))
#     M=list(range(8,17,1))
    
#     y_values_high_complex = []
#     y_values_grz = []
#     x1 = []
#     x2 = []
#     for i in range(len(L)) :
#         amount_beds_available_3= L[i]

#         amount_beds_available_4= M[i]
#         info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2,amount_of_runs, amount_beds_available_3, amount_beds_available_4,  percentage_2, amount_of_simulations,
#                             table_probability, table_arrival_rates, table_E_service_rate)
#         queue_2_waiting_time_3, h = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "High_Complex")
#         queue_2_waiting_time_4, g = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting_time_in_list_3", "GRZ")
#         print(queue_2_waiting_time_3,'is the waiting time for High complex cases with',L[i],'available beds and',j,'% shared beds')
#         print(queue_2_waiting_time_4,'is the waiting time for Geriatric Rehabilitation cases with',M[i],'available beds and',j,'% shared beds')
#         y_values_high_complex.append(queue_2_waiting_time_3)
#          y_values_grz.append(queue_2_waiting_time_4)
        
#         x1.append(L[i])
#         x2.append(M[i])
        
#     final_y1.append(y_values_high_complex)
#     final_x1.append(x1)
#     final_y2.append(y_values_grz)
#     final_x2.append(x2)
    
    
# plt.figure(figsize=(10, 6))   
# for i in range(len(final_x1)):
#     plt.plot(final_x1[i], final_y1[i],  label=f'High Complex for {(1+i)*5} shared beds' )    


# plt.title('E(Wq) for Different Numbers of Available Beds')
# plt.xlabel('Available Beds')
# plt.ylabel('Expected Waiting Time')
# plt.legend()
# plt.show()





# plt.figure(figsize=(10, 6))   
# for i in range(len(final_x2)):
#     plt.plot(final_x2[i], final_y2[i],  label=f'Geriatric Rehabilitation {(1+i)*5} shared beds' )
    

# plt.title('E(Wq) for Different Numbers of Available Beds')
# plt.xlabel('Available Beds')
# plt.ylabel('Expected Waiting Time')
# plt.legend()
# plt.show()



#constraint 1 ----------------------------------------------------------------------------------------
# amount beds 1 is for low complex, is in this code the target bed to check
c1_queue1_wait_1, c1_queue1_beds_1  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,amount_beds_available_2,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Low_Complex', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 

# #amount fo Respite_Care
c1_queue1_wait_2, c1_queue1_beds_2  = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_2,amount_beds_available_1,
                                                                  info_handled_elderly_queue_1, 'waiting_time', max_expected_waiting_time_1,
                                                                  amount_of_runs, amount_of_simulations, 'Respite_Care', percentage_1 ,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate) 

# #amount fo High_complex
c1_queue2_wait_3, c1_queue2_beds_3  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_3, amount_beds_available_4,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "High_Complex" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 

#Amount for GRZ
c1_queue2_wait_4, c1_queue2_beds_4  = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_4, amount_beds_available_3,
                                                                  info_handled_elderly_queue_2, 'waiting_time_in_list_3', max_expected_waiting_time_2,
                                                                  amount_of_runs, amount_of_simulations, "GRZ" ,percentage_2,
                                                                                          table_probability, table_arrival_rates, table_E_service_rate ) 

'''
#Average Service Time for Q1 and Q2    
for i in info_handled_elderly_queue_1:
    Sum_S_T1=0
    L1=[]
    for p in i:
        L1.append(p.service_time_elderly)
    for i in L1:
        Sum_S_T1+=i
    Sum_S_T1=Sum_S_T1/len(L1)
    print(Sum_S_T1)

for i in info_handled_elderly_queue_2:
    Sum_S_T2=0
    L2=[]
    for p in i:
        L2.append(p.service_time_elderly)
    for i in L2:
        Sum_S_T2+=i
    Sum_S_T2=Sum_S_T2/len(L2)
    print(Sum_S_T2)


#Average Waiting Time for Q1 and Q2
for amount_beds_available_1 in [10,20,30,40,50,70,90,100]:
    for i in queue_1_waiting_time_1:
        Sum_W_T1=0
        W1=[]
        for p in i:
            W1.append(p.waiting_time)
        for i in W1:
            Sum_W_T1+=i
        Sum_W_T1=Sum_W_T1/len(W1)
        print(Sum_W_T1)

for amount_beds_available_3 in [10,20,30,40,50,70,90,100]:
    for i in queue_2_waiting_time_1:
        Sum_W_T2=0
        W2=[]
        for p in i:
            W2.append(p.waiting_time)
        for i in W2:
            Sum_W_T2+=i
        Sum_W_T2=Sum_W_T2/len(W2)
        print(Sum_W_T2)
''' 


#TO DO 
# - Percentage of how often are all the beds occupied?
# - DONE - What is the percentage of people going from W2 to W3?  
# - Check how much average servise time is and compare with waiting for queue2
# - DONE (C1) - make parameter of percentage how many days should wait




















