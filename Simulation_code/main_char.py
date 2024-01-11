# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:13:06 2024

@author: charl
"""

# main.py
from functions import *
import pandas as pd
from main_char_queue_1 import simulation_qeueue_1
from main_char_queue_2 import simulation_qeueue_2


amount_of_runs = 1000
amount_beds_available_1 = 50
amount_beds_available_2 = 100

info_handled_elderly_queue_1 = simulation_qeueue_1(amount_of_runs,amount_beds_available_1)
info_handled_elderly_queue_2 = simulation_qeueue_2(amount_of_runs,amount_beds_available_2)

