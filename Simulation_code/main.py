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

class elderly:
  def __init__(self, care_level, medical,service_time_elderly, goes_where  ):
    self.care_level = care_level
    self.medical = medical
    self.service_time_elderly = service_time_elderly
    self.goes_where = goes_where
    self.days_in_bed = 0  # Initialize days_in_bed to 0
    self.waiting_time = 0  # Initialize days_in_bed to 0
    
    def increment_days_in_bed(self):
        self.days_in_bed += 1
    
    def increment_waiting_time(self):
        self.waiting_time += 1

 
table_probability = pd.read_excel('Outflow_probabilities.xlsx',index_col='Unnamed: 0')
table_arrival_rates = pd.read_excel('Arrival_rates.xlsx', index_col='Unnamed: 0')
table_E_service_rate = pd.read_excel('Service_Rates.xlsx',index_col='Unnamed: 0')
   

#TO DO NEXT IS LOOP TROUGH THE RIGHT POSSIBLE OPTIONS FOR QUEUE 1, AND QUEUE 2 
care_level = "Low_Complex"
medical = "General_Practitioner"


# Example usage
list_elderly_info = getting_info_elderly(table_probability, table_arrival_rates, table_E_service_rate, care_level, medical)

e1 = elderly(care_level, medical, list_elderly_info[2],list_elderly_info[3] )

