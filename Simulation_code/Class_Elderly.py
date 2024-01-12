# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:21:41 2024

@author: charl
"""



class elderly:
    def __init__(self, care_level, medical, service_time_elderly, goes_where, binary):
        self.care_level = care_level
        self.medical = medical
        self.service_time_elderly = service_time_elderly
        self.goes_where = goes_where
        self.through_waiting_2 = binary
        self.days_in_bed = 0  
        self.waiting_time = 0  
        self.waiting_time_in_list_3 = 0
    
    def increment_days_in_bed(self):
        self.days_in_bed += 1
    
    def increment_waiting_time(self):
        self.waiting_time += 1
        
    def increment_waiting_time_in_list_3(self):
        self.waiting_time_in_list_3 += 1
    
