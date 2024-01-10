# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:25:18 2024

@author: charl
"""


import pandas as pd
import numpy as np
from scipy.stats import gamma
from scipy import stats


excel_file_path = r"C:\Users\charl\OneDrive\Documents\VU vakken\OBP\procedures.csv"

df = pd.read_csv(excel_file_path)

list_situation_1_care = ["Low_complex, Respite_care"]
list_situation_1_medical = ['General_practitioner']


def arrivals_rate (situation, table, list_situation_1_care, list_situation_1_medical):
    
    
    for care in range(list_situation_1_care):
        for medical range (medical): 
            arrival_rate = table[care][medical]
        
    
