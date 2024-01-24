import streamlit as st
import plotly.express as px
import os
import time

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

##added
# from Simulation_code.functions_char import compute_expected_waiting_time_all_runs
# from Simulation_code.functions_char import multiple_simulations
from Simulation_code.main_char_queue_1 import simulation_qeueue_1
from Simulation_code.main_char_queue_2 import simulation_qeueue_2

st.set_page_config(
    # page_title='page1',
    # page_icon='📋',
    layout='wide',
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

amount_of_runs = 100
amount_of_simulations = 2

def compute_waiting_LC_RC(amount_beds_available_1, amount_beds_available_2, percentage_1, amount_of_runs, amount_of_simulations):
    #percentage_1 = shared beds lc rc
    info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1, amount_of_runs, amount_beds_available_1,
                                                        amount_beds_available_2, percentage_1, amount_of_simulations,
                                                        table_probability, table_arrival_rates, table_E_service_rate)

    queue_1_waiting_time_1 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time",
                                                                    "Low_Complex")
    queue_1_waiting_time_2 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time",
                                                                    "Respite_Care")

    return queue_1_waiting_time_1, queue_1_waiting_time_2

def compute_waiting_HC_GRZ(amount_beds_available_3, amount_beds_available_4, percentage_2, amount_of_runs, amount_of_simulations):
    #percentage_2 = shared beds hc grz
    info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2, amount_of_runs, amount_beds_available_3,
                                                        amount_beds_available_4, percentage_2, amount_of_simulations,
                                                        table_probability, table_arrival_rates, table_E_service_rate)

    queue_2_waiting_time_3 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2,
                                                                    "waiting_time_in_list_3", "High_Complex")
    queue_2_waiting_time_4 = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2,
                                                                    "waiting_time_in_list_3", "GRZ")
    return queue_2_waiting_time_3, queue_2_waiting_time_4


def main():
    cs_sidebar()

    tab1, tab2 = st.tabs(["LC & RC", "HC & GRZ"])

    with tab1:
        st.header('Low Complex & Respite Care')

        # Get the selected bed sharing option
        centralizing_option, bed_sharing_option = cs_scenario_selection()

        st.subheader('Input')

        if centralizing_option == 'Centralized':
            st.session_state.num_locations = 1
            num_low_complex_beds, num_respite_beds, num_shared_beds, num_nurses = body_input_low_respite(bed_sharing_option, st.session_state.num_locations)
            # input_low_respite(bed_sharing_option)

        if centralizing_option == 'Decentralized':
            add_location(bed_sharing_option)

        # Add a button to run the simulation
        if st.button("Run Simulation"):
            with st.container(border=True):
                st.subheader("Output")
                with st.status("In progress...") as status:
                    #Compute waiting times based on user inputs
                    queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_LC_RC(num_low_complex_beds,
                                                                                       num_respite_beds,
                                                                                       percentage_1=num_shared_beds,
                                                                                       amount_of_runs=amount_of_runs,
                                                                                       amount_of_simulations=amount_of_simulations)

                st.write('queue 1 waiting time: ', round(queue_1_waiting_time_1, 2), 'days')
                st.write('queue 2 waiting time: ', round(queue_1_waiting_time_2, 2), 'days')

            # run_simulation(selected_scenario, bed_sharing_option, centralizing_option)

        #Sensitivity analysis part
        st.header('Sensitivity Analysis')
        sensitivity_analysis(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs,
                             amount_of_simulations)

    with tab2:
        st.header('High Complex & GRZ Care')

        # Get the selected bed sharing option
        centralizing_option, bed_sharing_option = cs_scenario_selection()

        st.subheader('Input')
        if centralizing_option == 'Centralized':
            st.session_state.num_locations = 1
            num_high_complex_beds, num_grz_beds, num_shared_beds, num_nurses = body_input_low_respite(bed_sharing_option, st.session_state.num_locations)

        if centralizing_option == 'Decentralized':
            add_location(bed_sharing_option)

            # if bed_sharing_option == 'No bed sharing':
            #     input_low_respite(bed_sharing_option)

        # if selected_scenario == 'Low Complex & Respite Care':
        #     cs_body_low_respite(bed_sharing_option, centralizing_option)
        #     # plot_low_complex_chart()
        # elif selected_scenario == 'High Complex & Geriatric Rehabilitation':
        #     cs_body_high_complex(bed_sharing_option, centralizing_option)
        #     # plot_high_complex_chart()

        # Add a button to run the simulation
        if st.button("Run Simulation"):
            with st.status("In progress...") as status:
            # Compute waiting times based on user inputs
                queue_2_waiting_time_3, queue_2_waiting_time_4 = compute_waiting_HC_GRZ(num_high_complex_beds, num_grz_beds, percentage_1 = num_shared_beds, amount_of_runs = amount_of_runs,
                                                                             amount_of_simulations = amount_of_simulations)

            st.write('queue 1 waiting time: ', queue_2_waiting_time_3)
            st.write('queue 2 waiting time: ', queue_2_waiting_time_4)
            # run_simulation(selected_scenario, bed_sharing_option, centralizing_option)

        #Sensitivity analysis part
        st.header('Sensitivity Analysis')
        sensitivity_analysis(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs,
                             amount_of_simulations)

# def run_simulation(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs=1000, amount_of_simulations=1):
#     with st.spinner("In progress..."):  # as status:
#         # Compute waiting times based on user inputs
#         queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_LC_RC(num_low_complex_beds, num_respite_beds,
#                                                                                percentage_1=num_shared_beds,
#                                                                                amount_of_runs,
#                                                                                amount_of_simulations)
#     return queue_1_waiting_time_2, queue_1_waiting_time_2


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

def cs_bed_sharing_selection():
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Select a scenario", ['Bed sharing', 'No bed sharing'], key=f'low_respite_bed_radio')
    return bed_sharing_option

def cs_centralize_selection():
    # Display a radio button for centralize selection
    centralizing_option = st.radio("Centralize Option", ['Centralized', 'Decentralized'])
    return centralizing_option

def cs_scenario_selection():
    col1, col2 = st.columns(2)
    with col1:
        centralizing_option = cs_centralize_selection()
    with col2:
        bed_sharing_option = cs_bed_sharing_selection()

    return centralizing_option, bed_sharing_option

def add_location(bed_sharing_option):
    # for centeralized
    for i in range(st.session_state.num_locations):
        body_input_low_respite(bed_sharing_option, i)

    # Button to add a new location
    if st.button('Add Location', key = f'location_adding_button'):
        st.session_state.num_locations += 1

def body_input_low_respite(bed_sharing_option, index):

    # for i in range(num_locations):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # with col1:
        # st.write('Location name')
        # st.text_input('Location name', key=f'location_name_{i}', label_visibility='collapsed')
    with col1:
        st.write('Low complex beds')
        num_low_complex_beds = st.number_input('Number of low complex beds', min_value=0, max_value=None, value=8,
                                           key=f'low_complex_beds_{index}', label_visibility='collapsed')

    with col2:
        st.write('Respite care beds')
        num_respite_beds = st.number_input('Number of respite care beds', min_value=0, max_value=None, value=8, key=f'respite_beds_{index}',
                                   label_visibility='collapsed')

    with col1, col2:
        st.write('Number of beds one nurse can handle')

    with col3:
        st.write('Shared beds')
        disabled = bed_sharing_option == 'No bed sharing'
        num_shared_beds = st.number_input('Number of shared beds', min_value=0, max_value=None, value=0, key=f'shared_beds_{index}',
                        disabled=disabled, label_visibility='collapsed')

    with col4:
        st.write('Nurses')
        num_nurses = st.number_input('Number of nurses', min_value=0, max_value=None, value=2, key=f'nurses_{index}',
                        label_visibility='collapsed')

        st.number_input('Number of beds one nurse can handle', min_value=0, max_value=None, value=5,
                        key=f'nurses_load_{index}', label_visibility='collapsed')

    with col5:
        # st.write('Total beds')

        # Calculate the sum
        total_beds = num_low_complex_beds + num_respite_beds + num_shared_beds

        # Display the sum in a read-only style
        # st.markdown(f'<input type="text" value="{total_beds}" class="readonly-input" readonly>',
        #             unsafe_allow_html=True)

    with col6:
        # st.write('Total eff beds')

        # Calculate the sum
        eff_beds = (num_low_complex_beds + num_respite_beds + num_shared_beds) * num_nurses

        # Display the sum in a read-only style
        st.write('Total number of beds: ', total_beds)
        st.write('Total number of effective beds: ', eff_beds)
        # st.markdown(f'<input type="text" value="{eff_beds}" class="readonly-input" readonly>',
        #             unsafe_allow_html=True)

    return num_low_complex_beds, num_respite_beds, num_shared_beds, num_nurses


def sensitivity_analysis(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations):

    col1, col2 = st.columns(2)

    with col1:
        analysis_beds(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations)
    with col2:
        analysis_nurses()

    st.write('test test')

    with col2:
        st.write('test2')


def analysis_beds(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations):
    with st.container(border=True):
        st.subheader('Analysis beds')

        # Values slider for the number of beds
        bed_range = st.slider(
            'Select a range of values for the number of beds',
            1, 20, (5, 10))  # Adjust the range as needed

        # Button to trigger sensitivity analysis
        if st.button('Run Sensitivity Analysis for Beds'):
            # Lists to store data for plotting
            low_complex_waiting_times = []
            respite_waiting_times = []

            # Loop through different values of available beds
            for beds in range(bed_range[0], bed_range[1] + 1):
                # Compute waiting times based on user inputs
                queue_1_waiting_time_1, queue_1_waiting_time_2 = compute_waiting_LC_RC(num_low_complex_beds, num_respite_beds, num_shared_beds, amount_of_runs, amount_of_simulations)

                # Append data to lists for plotting
                low_complex_waiting_times.append(queue_1_waiting_time_1)
                respite_waiting_times.append(queue_1_waiting_time_2)

            # Plotting the sensitivity analysis results
            plot_sensitivity_analysis(bed_range, low_complex_waiting_times, respite_waiting_times)


import plotly.graph_objects as go


def plot_sensitivity_analysis(bed_range, low_complex_waiting_times, respite_waiting_times):
    fig = go.Figure()

    # Generate x values for the plot
    x_values = list(range(bed_range[0], bed_range[1] + 1))

    # Add traces for low complex and respite waiting times
    fig.add_trace(go.Scatter(x=x_values, y=low_complex_waiting_times, mode='lines', name='Low Complex'))
    fig.add_trace(go.Scatter(x=x_values, y=respite_waiting_times, mode='lines', name='Respite Care'))

    # Customize layout as needed
    fig.update_layout(title='Sensitivity Analysis',
                      xaxis_title='Number of Available Beds',
                      yaxis_title='Waiting Time',
                      legend_title='Scenarios')

    # Show the plot
    st.plotly_chart(fig)


# def plot_sensitivity_analysis(bed_range, low_complex_waiting_times, respite_waiting_times):
#     fig = px.line()
#
#     # Add traces for high complex and grz waiting times
#     fig.add_trace(px.line(x=bed_range, y=low_complex_waiting_times, name='Low Complex').data[0])
#     fig.add_trace(px.line(x=bed_range, y=respite_waiting_times, name='Respite care').data[0])
#
#     # Customize layout as needed
#     fig.update_layout(title='Sensitivity Analysis',
#                       xaxis_title='Number of Available Beds',
#                       yaxis_title='Waiting Time',
#                       legend_title='Scenarios')
#
#     # Show the plot
#     st.plotly_chart(fig)

def analysis_nurses():

    with st.container(border=True):
        st.subheader('Analysis nurses')

        st.slider('Select a range of values for number of nurses',
        0.0, 100.0, (10.0, 25.0))

def run_simulation(selected_scenario, bed_sharing_option):
    # Perform simulation based on selected_scenario and bed_sharing_option
    st.write('Simulation is running for:', selected_scenario)
    st.write('Bed Sharing Option:', bed_sharing_option)
    # Add simulation logic here


if __name__ == '__main__':
    main()