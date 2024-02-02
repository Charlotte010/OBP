import matplotlib.pyplot as plt
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
    layout='wide',
    initial_sidebar_state='collapsed'
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
    "Low_Complex": [7, 13, 15, 12, 7, 7],
    "Respite_Care": [6, 7, 9, 6, 6, 6]
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
amount_of_simulations = 15

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

    elif care_type == 'high_grz':
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

    return waiting_time_1, waiting_time_2

def cs_sidebar():
    global arrival_high_gp, arrival_high_ed, arrival_high_hospital, arrival_low_gp, arrival_respite_gp, arrival_grz_hospital
    # Add any sidebar components if needed
    with st.sidebar:
        st.write('Note: arrival rates are in days')

        st.write('**Low complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate from GP')
        with col2:
            arrival_low_gp = st.number_input('rate GP for low complex', min_value=0.0, max_value=None, value=1.34,
                            label_visibility='collapsed')

        st.write('**Respite care**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate from GP')
        with col2:
            arrival_respite_gp = st.number_input("rate GP respite", min_value=0.0, max_value=1.0, value=0.57,
                            label_visibility='collapsed')

        st.write('**High complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate from GP')
            st.write('Arrival rate from Emergency Department')
            st.write('Arrival rate from hospital')
        with col2:
            arrival_high_gp = st.number_input("rate GP high", min_value=0.0, max_value=None, value=1.34,
                            label_visibility='collapsed')
            arrival_high_ed= st.number_input("rate ED high", min_value=0.0, max_value=None, value=0.83,
                            label_visibility='collapsed')
            arrival_high_hospital=st.number_input("rate hospital high", min_value=0.0, max_value=None, value=0.94,
                            label_visibility='collapsed')

        st.write('**Geriatric rehabilitation**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate from hospital')
        with col2:
            arrival_grz_hospital = st.number_input("rate hospital Geriatric", min_value=0.0, max_value=None, value=0.54,
                            label_visibility='collapsed')

def cs_bed_sharing_selection(care_type):
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Select a scenario", ['Bed sharing', 'No bed sharing'], key=f'low_respite_bed_radio_{care_type}')
    return bed_sharing_option

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
        num_beds_1 = st.number_input('Number of beds', min_value=0, max_value=None, value=15, key= bed_type_1_key + care_type, label_visibility='collapsed')

    with col2:
        st.write(bed_type_2_label)
        num_beds_2 = st.number_input('Number of beds', min_value=0, max_value=None, value=5, key=bed_type_2_key, label_visibility='collapsed')

    with col3:
        st.write('Shared beds')
        disabled = bed_sharing_option == 'No bed sharing'

        num_shared_beds = st.number_input('Number of shared beds', min_value=0, max_value=None, value=0, key=shared_bed_key + str(index), disabled=disabled, label_visibility='collapsed')

        st.write('Beds per nurse:')

    with col4:
        st.write('Nurses')
        num_nurses = st.number_input('Number of nurses', min_value=0, max_value=None, value=2, key=nurses_key, label_visibility='collapsed')

        load_nurses = st.number_input('Number of beds one nurse can handle', min_value=0, max_value=None, value=5, key=f'nurses_load_{care_type}_{index}', label_visibility='collapsed')

    with col6:
        st.write('')
        # Calculate the sum
        total_beds = num_beds_1 + num_beds_2 + num_shared_beds
        eff_beds = load_nurses * num_nurses

        st.info(f"Total number of beds: {total_beds}\n \nTotal number of effective beds: {eff_beds}", icon="ℹ️")

    return num_beds_1, num_beds_2, num_shared_beds, num_nurses


def sensitivity_analysis(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        ####beds analysis
        with st.container(border=True):
            st.markdown('**Analysis Beds**')
            bed_range = st.slider('Select a range of values for number of beds',
                                  min_value=1, max_value=200, value=(1, 10), key= f'beds_range1{care_type}')
            bed_range_2 = st.slider('Select a range of values for number of second type beds',
                                    min_value=1, max_value=200, value=(1, 10), key=f'beds_range2{care_type}')

            if st.button("Run beds analysis", key = f'button_beds_{care_type}'):
                waiting_times_1, waiting_times_2, waiting_times_3 = analysis_beds(care_type, bed_range, bed_range_2,
                                                                num_shared_beds, amount_of_runs,
                                                                amount_of_simulations)
                plot_sensitivity_analysis(care_type, bed_range, bed_range_2, waiting_times_1,
                                          waiting_times_2, waiting_times_3)

    with col2:
        ####optimizing beds
        analysis_optimal_beds(care_type, num_beds_1, num_beds_2, num_shared_beds, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

    decentralization_analysis_calculation(care_type)
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

def analysis_optimal_beds(care_type, initial_beds_1, initial_beds_2, percentage, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate):
    with st.container(border=True):
        st.markdown('**Optimal beds**')

        col1, col2 = st.columns(2)
        with col1:
            st.write('Input a maximum amount of waiting days for a patient: ')

        with col2:
            max_waiting_time = st.number_input('Please input a maximum amount of waiting days for a patient: ',
                                                min_value=0.0, value=10.0, step=0.5, label_visibility='collapsed',
                                               key=f'max_waiting_time_{care_type}')

        if st.button('Find minimum number of beds', key=f'button_find_optimal_beds_{care_type}'):

            if care_type == 'low_respite':
                optimal_beds_1, optimal_beds_2, waiting_time_1, waiting_time_2 = optimize_bed_counts(care_type, 10, 3, percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
                st.write(f'Waiting time for low complex patients: ', round(waiting_time_1, 2), 'days')
                st.write(f'Optimal beds for low complex patients ', round(optimal_beds_1, 2), 'beds')
                st.write(f'Waiting time for respite care patients: ', round(waiting_time_2, 2), 'days')
                st.write(f'Optimal beds for respite care patients: ', round(optimal_beds_2, 2), 'beds')

            if care_type == 'high_grz':
                optimal_beds_1, optimal_beds_2, waiting_time_1, waiting_time_2 = optimize_bed_counts(care_type, 60, 7, percentage, max_waiting_time, amount_of_runs, amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)
                st.write(f'Waiting time for high complex patients: ', round(waiting_time_1, 2), 'days')
                st.write(f'Optimal beds for high complex patients ', round(optimal_beds_1, 2), 'beds')
                st.write(f'Waiting time for GRZ patients: ', round(waiting_time_2, 2), 'days')
                st.write(f'Optimal beds for GRZ patients: ', round(optimal_beds_2, 2), 'beds')

def analysis_beds(care_type, bed_range_1, bed_range_2, num_shared_beds, amount_of_runs, amount_of_simulations):
    waiting_times_1 = []
    waiting_times_2 = []
    waiting_times_3 = []

    for num_beds_1 in range(bed_range_1[0], bed_range_1[1] + 1):
        queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_times(care_type, num_beds_1, 0, num_shared_beds,
                                                                               amount_of_runs, amount_of_simulations)
        waiting_times_1.append(queue_1_waiting_time_1)

    for num_beds_2 in range(bed_range_2[0], bed_range_2[1] + 1):
        queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_times(care_type, 0, num_beds_2, num_shared_beds,
                                                               amount_of_runs, amount_of_simulations)
        waiting_times_2.append(queue_1_waiting_time_2)

    for num_beds_shared in range(bed_range_1[0]+bed_range_2[0], bed_range_1[1] +bed_range_2[1]+ 1):
        queue_1_waiting_time_shared, queue_1_waiting_time_2 = compute_waiting_times(care_type, 0, 0,
                                                                               num_beds_shared,
                                                                               amount_of_runs, amount_of_simulations)
        waiting_times_3.append(queue_1_waiting_time_shared)

    return waiting_times_1, waiting_times_2, waiting_times_3


def plot_sensitivity_analysis(care_type, bed_range_1, bed_range_2, waiting_times_1, waiting_times_2, waiting_times_3):

    col1, col2 = st.columns(2)

    with col1:

        plt.figure(figsize=(10, 6))

        beds_values_1 = np.arange(bed_range_1[0], bed_range_1[1] + 1)
        beds_values_2 = np.arange(bed_range_2[0], bed_range_2[1] + 1)

        if care_type == 'low_respite':
            plt.plot(beds_values_1, waiting_times_1, label='Low complex')
            plt.plot(beds_values_2, waiting_times_2, label='Respite care')

            plt.title(f'Waiting time vs number of beds', fontsize=22)
            plt.xlabel('Number of Beds', fontsize=18)
            plt.ylabel('Waiting Time (days)', fontsize=18)
            plt.legend()
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)

            st.pyplot(plt)

        if care_type == 'high_grz':
            plt.plot(beds_values_1, waiting_times_1, label=f'High complex')
            plt.plot(beds_values_2, waiting_times_2, label=f'GRZ')

            plt.title(f'Waiting time vs number of beds', fontsize=22)
            plt.xlabel('Number of Beds', fontsize=18)
            plt.ylabel('Waiting Time (days)', fontsize=18)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            plt.legend()

            st.pyplot(plt)

    with col2:
        #bed sharing plot
        plt.figure(figsize=(10, 6))

        beds_values_shared = np.arange(bed_range_1[0]+bed_range_2[0], bed_range_1[1] + bed_range_2[1] + 1)

        plt.plot(beds_values_shared, waiting_times_3)

        plt.title(f'Waiting time vs number of shared beds', fontsize=22)
        plt.xlabel('Number of Beds', fontsize=18)
        plt.ylabel('Waiting Time (days)', fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.legend()

        st.pyplot(plt)

def decentralization_analysis_layout(care_type):
    st.divider()
    # Define a template for a new analysis
    st.subheader(f'Decentralization Analysis')
    new_analysis_template = {
        'type1': {'num_beds': 8, 'num_nurses': 5},
        'type2': {'num_beds': 8, 'num_nurses': 5},
        'shared': {'num_beds': 8, 'num_nurses': 5}
    }

    # Customize labels based on care_type
    if care_type == 'low_respite':
        type1_label = 'Low Complex beds'
        type2_label = 'Respite beds'
    elif care_type == 'high_grz':
        type1_label = 'High Complex beds'
        type2_label = 'GRZ beds'

    # Initialize the session_state
    session_key = f'analyses_{care_type}'
    if session_key not in st.session_state:
        st.session_state[session_key] = [new_analysis_template.copy()]

    # Initialize lists to store the results
    list_locations_beds = []
    list_locations_nurses = []

    with st.container(border=True):


        # Add a button to trigger the display of additional analyses
        if st.button("Add location", key=f'button_add_location_{care_type}'):
            st.session_state[f'analyses_{care_type}'].append(new_analysis_template.copy())

        # Add a button to remove the latest analysis (only if there are additional analyses)
        if st.button("Remove location", key=f'button_remove_location_{care_type}') and len(st.session_state[f'analyses_{care_type}']) > 1:
            st.session_state[f'analyses_{care_type}'].pop()

        st.write('Number of beds 1 nurse can take care of')
        amount_beds_nurse_can_handle = st.number_input(f'Number of beds 1 nurse can take care of)', min_value=1, max_value=None,
                                                        key=f'{care_type}nurse_load', label_visibility='collapsed')

        # Get the maximum number of locations to determine the number of columns
        max_locations = max(len(st.session_state[f'analyses_{care_type}']), 1)

        # Display the analyses in a single row with separate tabs for each location
        for i in range(max_locations):
            with st.container():
                # Display location number above the columns
                st.markdown(f'**Location {i + 1}**')

                # Retrieve the specific analysis for this location
                analysis = st.session_state[f'analyses_{care_type}'][i]

                # Display the analyses in separate tabs
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(type1_label)

                    analysis['type1']['num_beds'] = st.number_input(f'Number of beds (Type 1 Analysis {i + 1})', min_value=0,
                                                                    max_value=None,
                                                                    value=analysis['type1']['num_beds'],
                                                                    key=f'{care_type}type1_beds{i + 1}',
                                                                    label_visibility='collapsed')
                    st.write('Amount of nurses')
                    analysis['type1']['num_nurses'] = st.number_input(f'Number of nurses (Type 1 Analysis {i + 1})',
                                                                      min_value=0, max_value=None,
                                                                      value=analysis['type1']['num_nurses'],
                                                                      key=f'{care_type}type1_nurses{i + 1}',
                                                                      label_visibility='collapsed')

                with col2:
                    st.write(type2_label)

                    analysis['type2']['num_beds'] = st.number_input(f'Number of beds (Type 2 Analysis {i + 1})', min_value=0,
                                                                    max_value=None,
                                                                    value=analysis['type2']['num_beds'],
                                                                    key=f'{care_type}type2_beds{i + 1}',
                                                                    label_visibility='collapsed')
                    st.write('Amount of nurses')
                    analysis['type2']['num_nurses'] = st.number_input(f'Number of nurses (Type 2 Analysis {i + 1})',
                                                                      min_value=0, max_value=None,
                                                                      value=analysis['type2']['num_nurses'],
                                                                      key=f'{care_type}type2_nurses{i + 1}',
                                                                      label_visibility='collapsed')

                with col3:
                    st.write('Shared beds')

                    analysis['shared']['num_beds'] = st.number_input(f'Number of shared beds (Analysis {i + 1})', min_value=0,
                                                                     max_value=None,
                                                                     value=analysis['shared']['num_beds'],
                                                                     key=f'{care_type}shared_beds{i + 1}',
                                                                     label_visibility='collapsed')
                    st.write('Amount of nurses')
                    analysis['shared']['num_nurses'] = st.number_input(f'Number of nurses for shared beds (Analysis {i + 1})',
                                                                       min_value=0, max_value=None,
                                                                       value=analysis['shared']['num_nurses'],
                                                                       key=f'{care_type}shared_nurses{i + 1}',
                                                                       label_visibility='collapsed')

            # Append data to lists
            beds_data = [analysis['type1']['num_beds'], analysis['type2']['num_beds'], analysis['shared']['num_beds']]
            nurses_data = [analysis['type1']['num_nurses'], analysis['type2']['num_nurses'],
                           analysis['shared']['num_nurses']]

            list_locations_beds.append(beds_data)
            list_locations_nurses.append(nurses_data)

        return list_locations_beds, list_locations_nurses, amount_beds_nurse_can_handle

def decentralization_analysis_calculation(care_type):
    list_locations_beds, list_locations_nurses, amount_beds_nurse_can_handle = decentralization_analysis_layout(care_type)

    list_beds = efficient_beds_per_care_level(list_locations_beds, list_locations_nurses, amount_beds_nurse_can_handle)
    if st.button("Run Simulation", key=f'button_run_simulation{care_type}'):
        result = compute_waiting_times(care_type, list_beds[0], list_beds[1], list_beds[2],
                          amount_of_runs, amount_of_simulations)


        # Display rounded results with custom messages
        if care_type == 'low_respite':
            st.write('Expected waiting time for low complex patients: ', round(result[0], 2), 'days')
            st.write('Expected waiting time for respite care patients: ', round(result[1], 2), 'days')
        elif care_type == 'high_grz':
            st.write('Expected waiting time for high complex patients: ', round(result[0], 2), 'days')
            st.write('Expected waiting time for GRZ patients: ', round(result[1], 2), 'days')

def main():
    st.header('Dashboard for Intermediate Care')

    # Define the tabs
    tab1, tab2 = st.tabs(["LC & RC", "HC & GRZ"])

    cs_sidebar()

    with tab1:
        care_type = 'low_respite'

        st.subheader('Low Complex & Respite Care')

        # Initialize variables with default values
        num_low_complex_beds = 0
        num_respite_beds = 0
        num_shared_beds = 0
        num_nurses = 0

        # Get the selected bed sharing option
        bed_sharing_option = cs_bed_sharing_selection(care_type)

        with st.container(border = True):
            st.subheader('Input')
            st.warning("""Warning: ensure minimum input of 15 beds for Low complex and 5 for Respite care to achieve reliable results""",
                icon="⚠️")

            num_low_complex_beds, num_respite_beds, num_shared_lcrc_beds, num_nurses_lcrc = body_input(
                    'low_respite', bed_sharing_option, index)

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

        #Sensitivity analysis part
        st.divider()
        st.subheader('Sensitivity Analysis')

        sensitivity_analysis(care_type, num_low_complex_beds, num_respite_beds, num_shared_lcrc_beds, amount_of_runs,
                             amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)

    with tab2:

        care_type = 'high_grz'

        st.subheader('High Complex & GRZ Care')

        # Initialize variables with default values
        num_high_complex_beds = 0
        num_grz_beds = 0
        num_shared_hcgrz_beds = 0
        num_nurses_hc = 0

        # Get the selected bed sharing option
        bed_sharing_option = cs_bed_sharing_selection(care_type)

        with st.container(border = True):
            st.subheader('Input')
            st.warning("""Warning: ensure minimum input of 70 beds for High complex and 10 for GRZ to achieve reliable results""",
                       icon="⚠️")

            num_high_complex_beds, num_grz_beds, num_shared_hcgrz_beds, num_nurses_hc = body_input(
                care_type, bed_sharing_option, index)

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
        st.subheader('Sensitivity Analysis')
        sensitivity_analysis(care_type, num_high_complex_beds, num_grz_beds, num_shared_hcgrz_beds, amount_of_runs,
                             amount_of_simulations, table_probability, table_arrival_rates, table_E_service_rate)


if __name__ == '__main__':
    main()