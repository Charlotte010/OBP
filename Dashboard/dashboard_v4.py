import streamlit as st
import plotly.express as px
import os
import plotly.graph_objects as go

import sys

global arrival_high_gp
global arrival_high_ed
global arrival_high_hospital
global arrival_low_gp
global arrival_respite_gp
global arrival_grz_hospital

arrival_high_gp = 1.34
arrival_high_ed = 0.83
arrival_high_hospital = 0.94
arrival_low_gp = 1.34
arrival_respite_gp = 0.57
arrival_grz_hospital = 0.54

os.chdir("C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP")
sys.path.append("C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP")


from Simulation_code.functions_char import *
import pandas as pd
from Simulation_code.main_char_queue_1 import simulation_qeueue_1
from Simulation_code.main_char_queue_2 import simulation_qeueue_2

st.set_page_config(
    # page_title='page1',
    # page_icon='📋',
    layout='wide',
    # current_tab = None,
    initial_sidebar_state='collapsed' #st.session_state.sidebar_state #'collapsed'
)
# Initialize the session state for the number of locations
if 'num_locations' not in st.session_state:
    st.session_state.num_locations = 1

#####################################
data = {
    "High_Complex": [0.578, 0.107, 0.198, 0.034, 0.023, 0.06],
    "GRZ": [0.6, 0.107, 0.21, 0.0, 0.023, 0.06],
    "Low_Complex": [0.7, 0.14, 0.1, 0.02, 0.02, 0.02],
    "Respite_Care": [0.9, 0.05, 0.03, 0.01, 0.005, 0.005]
}

# Index (row labels) for the table
index = ["Home", "Home_with_adjustments", "Long-term_care", "Geriatric_Rehabilitation", "Hospital_Care", "Death"]

# Creating the DataFrame
outflow_table = pd.DataFrame(data, index=index)

# Data for the Arrival Rate table
arrival_rate_data = {
    "High_Complex": [arrival_high_gp, arrival_high_ed, arrival_high_hospital],
    "GRZ": [0.0, 0.0, arrival_grz_hospital],
    "Low_Complex": [arrival_low_gp, 0.0, 0.0],
    "Respite_Care": [arrival_respite_gp, 0.0, 0.0]
}

# Index (row labels) for the Arrival Rate table
arrival_rate_index = ["General_Practitioner", "Emergency_Department", "Hospital"]

# Creating the DataFrame for Arrival Rates
arrival_rate_table = pd.DataFrame(arrival_rate_data, index=arrival_rate_index)

# Data for the Service Rates table
service_rate_data = {
    "High_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
    "GRZ": [31.1, 43.9, 47.8, 0.0, 22.9, 22.9],
    "Low_Complex": [31.1, 43.9, 47.8, 29.8, 22.9, 22.9],
    "Respite_Care": [14.0, 43.9, 47.8, 29.8, 22.9, 22.9]
}

# Index (row labels) for the Service Rates table
service_rate_index = ["Home", "Home_with_adjustments", "Long-term_care", "Geriatric_Rehabilitation",
                      "Hospital_Care", "Death"]

# Creating the DataFrame for Service Rates
service_rate_table = pd.DataFrame(service_rate_data, index=service_rate_index)
###################

table_probability = outflow_table
table_arrival_rates = arrival_rate_table
table_E_service_rate = service_rate_table

amount_of_runs = 1000
amount_of_simulations = 5

def compute_waiting_times(care_type, amount_beds_available_1, amount_beds_available_2, shared_beds_percentage, amount_of_runs, amount_of_simulations):
    if care_type == 'low_respite':
        simulation_queue = simulation_qeueue_1
        waiting_time_key_1, waiting_time_key_2 = "Low_Complex", "Respite_Care"
        info_handled_elderly_queue = multiple_simulations(simulation_queue, amount_of_runs, amount_beds_available_1,
                                                          amount_beds_available_2, shared_beds_percentage,
                                                          amount_of_simulations,
                                                          table_probability, table_arrival_rates, table_E_service_rate)

        waiting_time_1, _ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time",
                                                                   waiting_time_key_1)
        waiting_time_2, _ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time",
                                                                   waiting_time_key_2)

    elif care_type == 'high_grz':          #'HC_GRZ':
        simulation_queue = simulation_qeueue_2
        waiting_time_key_1, waiting_time_key_2 = "High_Complex", "GRZ"
        info_handled_elderly_queue = multiple_simulations(simulation_queue, amount_of_runs, amount_beds_available_1,
                                                          amount_beds_available_2, shared_beds_percentage,
                                                          amount_of_simulations,
                                                          table_probability, table_arrival_rates, table_E_service_rate)

        waiting_time_1, _ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time_in_list_3",
                                                                   waiting_time_key_1)
        waiting_time_2, _ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time_in_list_3",
                                                                   waiting_time_key_2)

    # info_handled_elderly_queue = multiple_simulations(simulation_queue, amount_of_runs, amount_beds_available_1,
    #                                                   amount_beds_available_2, shared_beds_percentage, amount_of_simulations,
    #                                                   table_probability, table_arrival_rates, table_E_service_rate)
    #
    # waiting_time_1,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time_in_list_3", waiting_time_key_1)
    # waiting_time_2,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, "waiting_time_in_list_3", waiting_time_key_2)

    return waiting_time_1, waiting_time_2

# def compute_waiting_LC_RC(amount_beds_available_1, amount_beds_available_2, percentage_1, amount_of_runs, amount_of_simulations):
#     """
#     Compute the waiting time for low complex and respite care
#     :param amount_beds_available_1: beds low complex
#     :param amount_beds_available_2: beds respite care
#     :param percentage_1: shared beds
#     :param amount_of_runs:
#     :param amount_of_simulations:
#     :return:
#     """
#     #percentage_1 = shared beds lc rc
#     info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1, amount_of_runs, amount_beds_available_1,
#                                                         amount_beds_available_2, percentage_1, amount_of_simulations,
#                                                         table_probability, table_arrival_rates, table_E_service_rate)
#
#     queue_1_waiting_time_1,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time",
#                                                                     "Low_Complex")
#     queue_1_waiting_time_2,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time",
#                                                                     "Respite_Care")
#     # print('Test')
#     # print(queue_1_waiting_time_1, queue_1_waiting_time_2)
#     # print('end test')
#
#     return queue_1_waiting_time_1, queue_1_waiting_time_2
#
# def compute_waiting_HC_GRZ(amount_beds_available_3, amount_beds_available_4, percentage_2, amount_of_runs, amount_of_simulations):
#     #percentage_2 = shared beds hc grz
#     info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2, amount_of_runs, amount_beds_available_3,
#                                                         amount_beds_available_4, percentage_2, amount_of_simulations,
#                                                         table_probability, table_arrival_rates, table_E_service_rate)
#
#     queue_2_waiting_time_3,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2,
#                                                                     "waiting_time_in_list_3", "High_Complex")
#     queue_2_waiting_time_4,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2,
#                                                                     "waiting_time_in_list_3", "GRZ")
#
#     return queue_2_waiting_time_3, queue_2_waiting_time_4

def cs_sidebar():
    global arrival_high_gp, arrival_high_ed, arrival_high_hospital, arrival_low_gp, arrival_respite_gp, arrival_grz_hospital
    # Add any sidebar components if needed
    with st.sidebar:
        st.write('**Low complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate GP')
            # st.write('Outflow home rate')
            # st.write('outflow home with adjustments rate')
            # st.write('Outflow long term care rate')
            # st.write('outflow geriatric care rate')
            # st.write('Outflow hospice rate')
            # st.write('outflow death rate')
        with col2:
            arrival_low_gp = st.number_input('rate GP for low complex', min_value=0.0, max_value=None, value=1.34,
                            label_visibility='collapsed')
            # st.number_input("home rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.7, label_visibility='collapsed')
            # st.number_input("home with adjustments rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.14, label_visibility='collapsed')
            # st.number_input("Outflow long term care rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.1, label_visibility='collapsed')
            # st.number_input("outflow geriatric care rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.02, label_visibility='collapsed')
            # st.number_input("Outflow hospice rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.02, label_visibility='collapsed')
            # st.number_input("Outflow death rate for low complex", min_value=0.0, max_value=1.0,
            #                 value=0.02, label_visibility='collapsed')

        st.write('**Respite care**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate')
            # st.write('Outflow home rate')
            # st.write('outflow home with adjustments rate')
            # st.write('Outflow long term care rate')
            # st.write('outflow geriatric care rate')
            # st.write('Outflow hospice rate')
            # st.write('outflow death rate')
        with col2:
            arrival_respite_gp = st.number_input("rate GP respite", min_value=0.0, max_value=1.0, value=0.57,
                            label_visibility='collapsed')
            # st.number_input("home rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.9, label_visibility='collapsed')
            # st.number_input("home with adjustments rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.05, label_visibility='collapsed')
            # st.number_input("Outflow long term care rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.03, label_visibility='collapsed')
            # st.number_input("outflow geriatric care rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.01, label_visibility='collapsed')
            # st.number_input("Outflow hospice rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.005, label_visibility='collapsed')
            # st.number_input("Outflow death rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.005, label_visibility='collapsed')

        st.write('**High complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate GP')
            st.write('Arrival rate Emergency Department')
            st.write('Arrival rate Hospital')
            # st.write('Outflow home rate')
            # st.write('outflow home with adjustments rate')
            # st.write('Outflow long term care rate')
            # st.write('outflow geriatric care rate')
            # st.write('Outflow hospice rate')
            # st.write('outflow death rate')
        with col2:
            arrival_high_gp = st.number_input("rate GP high", min_value=0.0, max_value=None, value=1.34,
                            label_visibility='collapsed')
            arrival_high_ed= st.number_input("rate ED high", min_value=0.0, max_value=None, value=0.83,
                            label_visibility='collapsed')
            arrival_high_hospital=st.number_input("rate hospital high", min_value=0.0, max_value=None, value=0.94,
                            label_visibility='collapsed')
            # st.number_input("home rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.578, label_visibility='collapsed')
            # st.number_input("home with adjustments rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.107, label_visibility='collapsed')
            # st.number_input("Outflow long term care rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.198, label_visibility='collapsed')
            # st.number_input("outflow geriatric care rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.034, label_visibility='collapsed')
            # st.number_input("Outflow hospice rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.023, label_visibility='collapsed')
            # st.number_input("Outflow death rate respite", min_value=0.0, max_value=1.0,
            #                 value=0.06, label_visibility='collapsed')

        st.write('**Geriatric rehabilitation**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate hospital')
            # st.write('Outflow home rate')
            # st.write('outflow home with adjustments rate')
            # st.write('Outflow long term care rate')
            # st.write('outflow geriatric care rate')
            # st.write('Outflow hospice rate')
            # st.write('outflow death rate')
        with col2:
            arrival_grz_hospital = st.number_input("rate hospital Geriatric", min_value=0.0, max_value=None, value=0.54,
                            label_visibility='collapsed')
            # st.number_input("home rate Geriatric", min_value=0.0, max_value=1.0,
            #                 value=0.6, label_visibility='collapsed')
            # st.number_input("home with adjustments rate Geriatric", min_value=0.0, max_value=1.0,
            #                 value=0.107, label_visibility='collapsed')
            # st.number_input("Outflow long term care rate Geriatric", min_value=0.0, max_value=1.0,
            #                 value=0.21, label_visibility='collapsed')
            # st.number_input("outflow geriatric care rate Geriatric", min_value=0.0, max_value=0.0,
            #                 value=0.0, label_visibility='collapsed')  # not possible
            # st.number_input("Outflow hospice rate Geriatric", min_value=0.0, max_value=1.0,
            #                 value=0.023, label_visibility='collapsed')
            # st.number_input("Outflow death rate Geriatric", min_value=0.0, max_value=1.0,
            #                 value=0.06, label_visibility='collapsed')

def cs_bed_sharing_selection(care_type):
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Select a scenario", ['Bed sharing', 'No bed sharing'], key=f'low_respite_bed_radio_{care_type}')
    return bed_sharing_option

def cs_centralize_selection(care_type):
    # Display a radio button for centralize selection
    centralizing_option = st.radio("Centralize Option", ['Centralized', 'Decentralized'], key=f'central_radio_{care_type}')
    return centralizing_option

def cs_scenario_selection(care_type):
    col1, col2 = st.columns(2)
    with col1:
        centralizing_option = cs_centralize_selection(care_type)
    with col2:
        bed_sharing_option = cs_bed_sharing_selection(care_type)

    return centralizing_option, bed_sharing_option

def add_location(care_type, bed_sharing_option):#, key):
    for i in range(st.session_state.num_locations):
        if care_type == 'low_respite':
            body_input(care_type, bed_sharing_option, i)
        elif care_type == 'high_grz': #'HC_GRZ':
            body_input(care_type, bed_sharing_option, i)

    # Button to add a new location
    if st.button('Add Location', key=f'location_adding_button_{care_type}'):
        st.session_state.num_locations += 1

# def add_location(bed_sharing_option, key):
#     # for centeralized
#     for i in range(st.session_state.num_locations):
#         body_input(care_type, i)
#         # body_input_low_respite(bed_sharing_option, i)
#
#     # Button to add a new location
#     if st.button('Add Location', key = f'location_adding_button_{key}'):
#         st.session_state.num_locations += 1
#
# def add_location_hc_grz(bed_sharing_option,key):
#     """
#     decenteralization option
#     :param bed_sharing_option:
#     :return: None
#     """
#     for i in range(st.session_state.num_locations):
#         body_input_high_grz(bed_sharing_option, i)
#
#     # Button to add a new location
#     if st.button('Add Location', key = f'location_adding_button_{key}'):
#         st.session_state.num_locations += 1

def body_input(care_type, bed_sharing_option, index):
    # Initialize variables to ensure they are always set
    bed_type_1_label, bed_type_2_label, shared_bed_key = '', '', ''

    # Define labels and keys based on care_type
    if care_type == 'low_respite':
        bed_type_1_label = 'Low complex beds'
        bed_type_2_label = 'Respite care beds'
        shared_bed_key = 'shared_beds_lcrc_'
    elif care_type == 'high_grz':
        bed_type_1_label = 'High complex beds'
        bed_type_2_label = 'GRZ beds'
        shared_bed_key = 'shared_beds_hcgrz_'

    bed_type_1_key = f'{care_type}_beds_1_{index}'
    bed_type_2_key = f'{care_type}_beds_2_{index}'
    nurses_key = f'nurses_{care_type}_{index}'

    col1, col2, col3, col4, col5, col6 = st.columns([0.15, 0.15, 0.15, 0.15, 0.05, 0.3])

    with col1:
        st.write(bed_type_1_label)
        num_beds_1 = st.number_input('Number of beds', min_value=0, max_value=None, value=8, key=bed_type_1_key, label_visibility='collapsed')

    with col2:
        st.write(bed_type_2_label)
        num_beds_2 = st.number_input('Number of beds', min_value=0, max_value=None, value=8, key=bed_type_2_key, label_visibility='collapsed')

    with col3:
        st.write('Shared beds')
        disabled = bed_sharing_option == 'No bed sharing'
        # print("Widget key:", shared_bed_key + str(index))  # Debugging line

        num_shared_beds = st.number_input('Number of shared beds', min_value=0, max_value=None, value=0, key=shared_bed_key + str(index), disabled=disabled, label_visibility='collapsed')
        # num_shared_beds = st.number_input('Number of shared beds', min_value=0, max_value=None, value=0,
        #                                   key=shared_bed_key + str(index),
        #                                   label_visibility='collapsed')

    with col4:
        st.write('Nurses')
        num_nurses = st.number_input('Number of nurses', min_value=0, max_value=None, value=2, key=nurses_key, label_visibility='collapsed')
        st.number_input('Number of beds one nurse can handle', min_value=0, max_value=None, value=5, key=f'nurses_load_{care_type}_{index}', label_visibility='collapsed')

    with col6:
        st.write('')
        # Calculate the sum
        total_beds = num_beds_1 + num_beds_2 + num_shared_beds
        eff_beds = (num_beds_1 + num_beds_2 + num_shared_beds) * num_nurses

        st.info(f"Total number of beds: {total_beds}\n \nTotal number of effective beds: {eff_beds}", icon="ℹ️")

    return num_beds_1, num_beds_2, num_shared_beds, num_nurses


# def sensitivity_analysis(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
#
#     col1, col2 = st.columns([0.7, 0.3])
#
#     with col1:
#         with st.container(border=True):
#             st.subheader('Analysis Beds')
#             bed_range = st.slider('Select a range of values for number of beds',
#                                   min_value=10, max_value=100, value=(num_low_complex_beds, 1))
#             respite_bed_range = st.slider('Select a range of values for number of respite care beds',
#                                           min_value=10, max_value=100, value=(1, num_respite_beds))
#
#             if st.button("Run Sensitivity Analysis"):
#                 low_complex_waiting_times, respite_waiting_times = analysis_beds(bed_range, respite_bed_range,
#                                                                                  num_shared_beds, amount_of_runs,
#                                                                                  amount_of_simulations)
#                 plot_sensitivity_analysis(bed_range, respite_bed_range, low_complex_waiting_times,
#                                           respite_waiting_times)
#     with col2:
#         analysis_optimal_beds(simulation_qeueue_1, num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

def sensitivity_analysis(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        ####beds analysis
        with st.container(border=True):
            st.subheader('Analysis Beds')
            bed_range = st.slider('Select a range of values for number of beds',
                                  min_value=1, max_value=100, value=(1, 10), key= f'beds_range1{care_type}')
            bed_range_2 = st.slider('Select a range of values for number of second type beds',
                                    min_value=1, max_value=100, value=(1, 10), key=f'beds_range2{care_type}')

            if st.button("Run beds analysis", key = f'button_beds_{care_type}'):
                waiting_times_1, waiting_times_2 = analysis_beds(care_type, bed_range, bed_range_2,
                                                                num_shared_beds, amount_of_runs,
                                                                amount_of_simulations)
                plot_sensitivity_analysis(care_type, bed_range, bed_range_2, waiting_times_1,
                                          waiting_times_2)

    with col2:
        ####optimizing beds
        analysis_optimal_beds(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

def optimize_bed_counts(care_type, initial_beds_1, initial_beds_2, shared_beds_percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
    optimal_beds_1 = initial_beds_1
    optimal_beds_2 = initial_beds_2

    # Loop until both waiting times are below the maximum
    while True:
        if care_type == 'low_respite':
            waiting_time_1, waiting_time_2 = compute_waiting_times('low_respite', optimal_beds_1, optimal_beds_2, shared_beds_percentage, amount_of_runs, amount_of_simulations)
        elif care_type == 'high_grz':
            waiting_time_1, waiting_time_2 = compute_waiting_times('high_grz', optimal_beds_1, optimal_beds_2, shared_beds_percentage, amount_of_runs, amount_of_simulations)

        if waiting_time_1 <= max_waiting_time and waiting_time_2 <= max_waiting_time:
            break

        if waiting_time_1 > max_waiting_time:
            optimal_beds_1 += 1
        if waiting_time_2 > max_waiting_time:
            optimal_beds_2 += 1

    return optimal_beds_1, optimal_beds_2, waiting_time_1, waiting_time_2


# def optimize_bed_counts(simulation_queue, initial_beds_lc, initial_beds_rc, percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
#     optimal_beds_lc = initial_beds_lc
#     optimal_beds_rc = initial_beds_rc
#
#     # Initial simulation
#     info_queue = multiple_simulations(simulation_queue, amount_of_runs, optimal_beds_lc, optimal_beds_rc, percentage, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
#
#     # Calculate initial waiting times
#     waiting_time_lc,_ = compute_expected_waiting_time_all_runs(info_queue, "waiting_time", "Low_Complex")
#     waiting_time_rc,_ = compute_expected_waiting_time_all_runs(info_queue, "waiting_time", "Respite_Care")
#
#     # Loop until both waiting times are below the maximum
#     while waiting_time_lc > max_waiting_time or waiting_time_rc > max_waiting_time:
#         if waiting_time_lc > max_waiting_time:
#             optimal_beds_lc += 1
#         if waiting_time_rc > max_waiting_time:
#             optimal_beds_rc += 1
#
#         # Re-run simulation with updated bed counts
#         info_queue = multiple_simulations(simulation_queue, amount_of_runs, optimal_beds_lc, optimal_beds_rc, percentage, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
#
#         # Recalculate waiting times
#         waiting_time_lc,_ = compute_expected_waiting_time_all_runs(info_queue, "waiting_time", "Low_Complex")
#         waiting_time_rc,_ = compute_expected_waiting_time_all_runs(info_queue, "waiting_time", "Respite_Care")
#         print(waiting_time_rc, waiting_time_lc, max_waiting_time)
#
#     return optimal_beds_lc, optimal_beds_rc, waiting_time_lc, waiting_time_rc

def analysis_optimal_beds(care_type, initial_beds_1, initial_beds_2, percentage, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
    with st.container(border=True):
        st.subheader('Optimal beds')

        col1, col2 = st.columns(2)
        with col1:
            st.write('Input a maximum amount of waiting days for a patient: ')

        with col2:
            max_waiting_time = st.number_input('Please input a maximum amount of waiting days for a patient: ',
                                                min_value=0.0, value=10.0, step=0.5, label_visibility='collapsed',
                                               key=f'max_waiting_time_{care_type}')

        if st.button('Find minimum number of beds', key=f'button_find_optimal_beds_{care_type}'):
            optimal_beds_1, optimal_beds_2, waiting_time_1, waiting_time_2 = optimize_bed_counts(care_type, initial_beds_1, initial_beds_2, percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

            st.write(f'Waiting time for {care_type} type 1: ', round(waiting_time_1, 2), 'days')
            st.write(f'Beds for {care_type} type 1: ', round(optimal_beds_1, 2), 'beds')
            st.write(f'Waiting time for {care_type} type 2: ', round(waiting_time_2, 2), 'days')
            st.write(f'Beds for {care_type} type 2: ', round(optimal_beds_2, 2), 'beds')


# def analysis_optimal_beds(simulation_queue, initial_beds_lc, initial_beds_rc, percentage, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
#
#     with st.container(border=True):
#         st.subheader('Optimal beds')
#
#         col1, col2 = st.columns(2)
#         with col1:
#             st.write('Input a maximum amount of waiting days for a patient: ')
#
#         with col2:
#             max_waiting_time = st.number_input('Please input a maximum amount of waiting days for a patient: ',
#                                                 min_value=0.0, value=10.0, step = 0.5, label_visibility='collapsed')
#
#         if st.button('Find minimum number of beds'):
#             optimal_beds_lc, optimal_beds_rc, waiting_time_lc, waiting_time_rc = optimize_bed_counts(simulation_queue, initial_beds_lc, initial_beds_rc, percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
#
#             st.write('waiting time low complex care: ', round(waiting_time_lc,2), 'days')
#             st.write('Beds low complex care: ', round(optimal_beds_lc,2), 'days')
#             st.write('waiting time respite care: ', round(waiting_time_rc,2), 'days')
#             st.write('Beds respite care: ', round(optimal_beds_rc,2), 'days')

    # return optimal_beds_lc, optimal_beds_rc, waiting_time_lc, waiting_time_rc

# def analysis_beds(bed_range, respite_bed_range, num_shared_beds, amount_of_runs, amount_of_simulations):
#     low_complex_waiting_times = []
#     respite_waiting_times = []
#
#     for num_low_complex_beds in range(bed_range[0], bed_range[1] + 1):
#         # Perform simulation for each low-complexity bed configuration
#         queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_LC_RC(
#             num_low_complex_beds, 0, num_shared_beds, amount_of_runs, amount_of_simulations)
#
#         low_complex_waiting_times.append(queue_1_waiting_time_1)
#         # Append the waiting time directly, not as a list
#         # low_complex_waiting_times.append(queue_1_waiting_time_1)
#
#     for num_respite_care_beds in range(respite_bed_range[0], respite_bed_range[1] + 1):
#         # Perform simulation for each respite care bed configuration
#         queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_LC_RC(
#             0, num_respite_care_beds, num_shared_beds, amount_of_runs, amount_of_simulations)
#
#         respite_waiting_times.append(queue_1_waiting_time_2)
#         # Append the waiting time directly, not as a list
#         # respite_waiting_times.append(queue_1_waiting_time_2)
#
#     return low_complex_waiting_times, respite_waiting_times

def analysis_beds(care_type, bed_range_1, bed_range_2, num_shared_beds, amount_of_runs, amount_of_simulations):
    waiting_times_1 = []
    waiting_times_2 = []

    for num_beds_1 in range(bed_range_1[0], bed_range_1[1] + 1):
        queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_times(care_type, num_beds_1, 0, num_shared_beds,
                                                                               amount_of_runs, amount_of_simulations)

        waiting_times_1.append(queue_1_waiting_time_1)

    for num_beds_2 in range(bed_range_2[0], bed_range_2[1] + 1):
        queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_times(care_type, 0, num_beds_2, num_shared_beds,
                                                               amount_of_runs, amount_of_simulations)
            # if care_type == 'low_respite':
            #     # Assuming compute_waiting_LC_RC is already adapted for care_type
            #     waiting_time_1, waiting_time_2 = compute_waiting_times(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations)
            # elif care_type == 'high_grz':
            #     # Assuming compute_waiting_HC_GRZ is already adapted for care_type
            #     waiting_time_1, waiting_time_2 = compute_waiting_times(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations)

        waiting_times_2.append(queue_1_waiting_time_2)

    return waiting_times_1, waiting_times_2


def plot_sensitivity_analysis(care_type, bed_range_1, bed_range_2, waiting_times_1, waiting_times_2):
    plt.figure(figsize=(10, 6))

    beds_values_1 = np.arange(bed_range_1[0], bed_range_1[1] + 1)
    beds_values_2 = np.arange(bed_range_2[0], bed_range_2[1] + 1)

    st.write(len(beds_values_1), len(waiting_times_1))
    st.write(len(beds_values_2), len(waiting_times_2))

    plt.plot(beds_values_1, waiting_times_1, label=f'{care_type} Type 1 Waiting Time')
    plt.plot(beds_values_2, waiting_times_2, label=f'{care_type} Type 2 Waiting Time')

    plt.title(f'Sensitivity Analysis for {care_type} - Number of Beds')
    plt.xlabel('Number of Beds')
    plt.ylabel('Waiting Time (days)')
    plt.legend()

    st.pyplot(plt)


# def plot_sensitivity_analysis(bed_range, respite_bed_range, low_complex_waiting_times, respite_waiting_times):
#     plt.figure(figsize=(10, 6))
#
#     beds_values = np.arange(bed_range[0], bed_range[1] + 1)
#     respite_beds_values = np.arange(respite_bed_range[0], respite_bed_range[1] + 1)
#
#     plt.plot(beds_values, low_complex_waiting_times, label='Low Complex Waiting Time')
#     plt.plot(respite_beds_values, respite_waiting_times, label='Respite Waiting Time')
#
#     plt.title('Sensitivity Analysis - Number of Beds')
#     plt.xlabel('Number of Beds')
#     plt.ylabel('Waiting Time (days)')
#     plt.legend()
#
#     st.pyplot(plt)


def c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1, amount_beds_available_2,
                                    info_handled_elderly_queue, waiting,
                                    max_waiting_time, amount_of_runs, amount_of_simulations, care_level,
                                    percentage,
                                    table_probability, table_arrival_rates, table_E_service_rate):

    queue_1_waiting_time,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)

    while queue_1_waiting_time > max_waiting_time or queue_1_waiting_time > max_waiting_time:
        amount_beds_available_1 += 1
        amount_beds_available_2 += 1

        info_handled_elderly_queue = multiple_simulations(simulation_qeueue_1, amount_of_runs, amount_beds_available_1,
                                                          amount_beds_available_2, percentage, amount_of_simulations,
                                                          table_probability, table_arrival_rates, table_E_service_rate)

        queue_1_waiting_time,_ = compute_expected_waiting_time_all_runs(info_handled_elderly_queue, waiting, care_level)

    return queue_1_waiting_time, amount_beds_available_1

# def find_optimal_beds(simulation_queue_1, simulation_queue_2, initial_beds_1, initial_beds_2, max_waiting_time, amount_of_runs, amount_of_simulations, care_level, percentage, table_probability, table_arrival_rates, table_E_service_rate):
#     amount_beds_available_1 = initial_beds_1
#     amount_beds_available_2 = initial_beds_2
#
#     # Initialize variables to store the waiting times for both queues
#     waiting_time_1 = float('inf')
#     waiting_time_2 = float('inf')
#
#     # Keep increasing the beds for queue 1 and queue 2 until the waiting times are below the max_waiting_time
#     while waiting_time_1 > max_waiting_time or waiting_time_2 > max_waiting_time:
#         # Increase the bed count for queue 1 and queue 2
#         amount_beds_available_1 += 1
#         amount_beds_available_2 += 1
#
#         # Run the simulation for the new bed counts
#         info_handled_elderly_queue_1 = multiple_simulations(simulation_queue_1, amount_of_runs, amount_beds_available_1, amount_beds_available_2, percentage, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
#         info_handled_elderly_queue_2 = multiple_simulations(simulation_queue_2, amount_of_runs, amount_beds_available_1, amount_beds_available_2, percentage, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
#
#         # Compute the waiting times for both queues
#         waiting_time_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting", care_level)
#         waiting_time_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2, "waiting", care_level)
#
#     return amount_beds_available_1, amount_beds_available_2, waiting_time_1, waiting_time_2

def decenteralization_analysis():
    return None

def main():

    # Define the tabs
    tab1, tab2 = st.tabs(["LC & RC", "HC & GRZ"])

    cs_sidebar()

    with tab1:
        care_type = 'low_respite'
        # key = 'LCRC'
        st.header('Low Complex & Respite Care')

        # Initialize variables with default values
        num_low_complex_beds = 0
        num_respite_beds = 0
        num_shared_beds = 0
        num_nurses = 0

        # Get the selected bed sharing option
        centralizing_option, bed_sharing_option = cs_scenario_selection(care_type)

        with st.container(border = True):
            st.subheader('Input')

            if centralizing_option == 'Centralized':
                st.session_state.num_locations = 1
                num_low_complex_beds, num_respite_beds, num_shared_lcrc_beds, num_nurses_lcrc = body_input(
                    'low_respite', bed_sharing_option, index)

                # num_low_complex_beds, num_respite_beds, num_shared_beds, num_nurses = body_input_low_respite(bed_sharing_option, st.session_state.num_locations)

            if centralizing_option == 'Decentralized':
                add_location('low_respite', bed_sharing_option)#, key)

                # add_location(bed_sharing_option, key)

            if bed_sharing_option == 'No bed sharing':
                num_shared_lcrc_beds = 0

        # Add a button to run the simulation
        if st.button("Run Simulation", key = f'simulation_button_{care_type}'):
            with st.container(border=True):
                st.subheader("Output")
                with st.status("In progress...") as status:
                    st.write(f'Running for {amount_of_runs} runs and {amount_of_simulations} simulations')
                    #Compute waiting times based on user inputs
                    # For Low Complex & Respite Care
                    queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_times('low_respite',
                                                                                           num_low_complex_beds,
                                                                                           num_respite_beds,
                                                                                           num_shared_lcrc_beds,
                                                                                           amount_of_runs,
                                                                                           amount_of_simulations)

                st.write('Expected waiting time for low complex patients: ', round(queue_1_waiting_time_1, 2), 'days')
                st.write('Expected waiting time for respite care patients: ', round(queue_1_waiting_time_2, 2), 'days')


            # run_simulation(selected_scenario, bed_sharing_option, centralizing_option)

        #Sensitivity analysis part
        st.divider()
        st.header('Sensitivity Analysis')

        sensitivity_analysis(care_type, num_low_complex_beds, num_respite_beds, num_shared_lcrc_beds, amount_of_runs,
                             amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

        # sensitivity_analysis(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs,
        #                      amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

    with tab2:

        care_type = 'high_grz'
        # key = 'HCGRZ'

        st.header('High Complex & GRZ Care')

        # Initialize variables with default values
        num_high_complex_beds = 0
        num_grz_beds = 0
        num_shared_hcgrz_beds = 0
        num_nurses_hc = 0

        # Get the selected bed sharing option
        centralizing_option, bed_sharing_option = cs_scenario_selection(care_type)

        with st.container(border = True):
            st.subheader('Input')

            if centralizing_option == 'Centralized':
                st.session_state.num_locations = 1
                # num_high_complex_beds, num_grz_beds, num_shared_hcgrz_beds, num_nurses_hc = body_input_high_grz(bed_sharing_option, st.session_state.num_locations)
                num_high_complex_beds, num_grz_beds, num_shared_hcgrz_beds, num_nurses_hcgrz = body_input('high_grz',
                                                                                                          bed_sharing_option,
                                                                                                          index)

            if centralizing_option == 'Decentralized':
                # add_location_hc_grz(bed_sharing_option,key)
                add_location('high_grz', bed_sharing_option)#, key)

            if bed_sharing_option == 'No bed sharing':
                num_shared_hcgrz_beds = 0

        # Add a button to run the simulation
        if st.button("Run Simulation", key = f'simulation_button_{care_type}'):
            with st.container(border=True):
                st.subheader("Output")
                with st.status("In progress...") as status:
                    st.write(f'Running for {amount_of_runs} runs and {amount_of_simulations} simulations')
                    #Compute waiting times based on user inputs
                    queue_2_waiting_time_3, queue_2_waiting_time_4 = compute_waiting_times('high_grz',
                                                                                           num_high_complex_beds,
                                                                                           num_grz_beds,
                                                                                           num_shared_hcgrz_beds,
                                                                                           amount_of_runs,
                                                                                           amount_of_simulations)

                st.write('Expected waiting time for high complex patients: ', round(queue_2_waiting_time_3, 2), 'days')
                st.write('Expected waiting time for GRZ patients: ', round(queue_2_waiting_time_4, 2), 'days')


        # Sensitivity analysis part
        st.divider()
        st.header('Sensitivity Analysis')
        sensitivity_analysis(care_type, num_high_complex_beds, num_grz_beds, num_shared_hcgrz_beds, amount_of_runs,
                             amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)


if __name__ == '__main__':
    main()