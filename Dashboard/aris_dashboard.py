import streamlit as st
import plotly.express as px
import os

import sys
# Add project_root to the Python path if it's not already there
from pathlib import Path

os.chdir("C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP")

sys.path.append("C:\\Users\\zerin\\OneDrive\\Documenten\\Project OBP\\OBP")

from Simulation_code.functions import *
import pandas as pd
from Simulation_code.main_queue_1 import simulation_qeueue_1
from Simulation_code.main_queue_2 import simulation_qeueue_2
from Simulation_code import *


def compute_waiting(amount_beds_available_1, amount_beds_available_2, max_expected_waiting_time_1,
                    max_expected_waiting_time_2, amount_of_runs=1000, amount_of_simulations=1):
    info_handled_elderly_queue_1 = multiple_simulations(simulation_qeueue_1, amount_of_runs, amount_beds_available_1,
                                                        amount_of_simulations)
    info_handled_elderly_queue_2 = multiple_simulations(simulation_qeueue_2, amount_of_runs, amount_beds_available_2,
                                                        amount_of_simulations)

    c1_queue1_wait, c1_queue1_beds = c1_on_max_expected_waiting_time(simulation_qeueue_1, amount_beds_available_1,
                                                                     info_handled_elderly_queue_1, 'waiting_time',
                                                                     max_expected_waiting_time_1, amount_of_runs,
                                                                     amount_of_simulations)

    c1_queue2_wait, c1_queue2_beds = c1_on_max_expected_waiting_time(simulation_qeueue_2, amount_beds_available_2,
                                                                     info_handled_elderly_queue_2,
                                                                     'waiting_time_in_list_3',
                                                                     max_expected_waiting_time_2, amount_of_runs,
                                                                     amount_of_simulations)

    queue_1_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_1, "waiting_time")
    queue_2_waiting_time = compute_expected_waiting_time_all_runs(info_handled_elderly_queue_2,
                                                                  "waiting_time_in_list_3")

    return queue_1_waiting_time, queue_2_waiting_time


def main_test():
    cs_sidebar()

    # Input parameters using Streamlit widgets
    amount_beds_available_1 = st.slider("Beds available in Queue 1", 0, 100, 50)
    amount_beds_available_2 = st.slider("Beds available in Queue 2", 0, 200, 160)
    max_expected_waiting_time_1 = st.slider("Max waiting time in Queue 1", 0, 10, 3)
    max_expected_waiting_time_2 = st.slider("Max waiting time in Queue 2", 0, 10, 5)

    # Compute waiting times based on user inputs
    queue_1_waiting_time, queue_2_waiting_time = compute_waiting(amount_beds_available_1, amount_beds_available_2,
                                                                 max_expected_waiting_time_1,
                                                                 max_expected_waiting_time_2)

    st.write('queue 1 waiting time: ', queue_1_waiting_time)
    st.write('queue 2 waiting time: ', queue_2_waiting_time)

    # Get the selected scenario
    selected_scenario = cs_scenario_selection()

    # Get the selected bed sharing option
    bed_sharing_option = cs_bed_sharing_selection()
    centralizing_option = cs_centralize_selection()

    if selected_scenario == 'Low Complex & Respite Care':
        cs_body_low_respite(bed_sharing_option, centralizing_option)
        plot_low_complex_chart()
    elif selected_scenario == 'High Complex & Geriatric Rehabilitation':
        cs_body_high_complex(bed_sharing_option, centralizing_option)
        plot_high_complex_chart()

    # Add a button to run the simulation
    if st.button("Run Simulation"):
        run_simulation(selected_scenario, bed_sharing_option, centralizing_option)


def cs_sidebar():
    # Add any sidebar components if needed
    pass


def cs_scenario_selection():
    # Display a radio button for scenario selection
    selected_scenario = st.radio("Select Scenario",
                                 ['Low Complex & Respite Care', 'High Complex & Geriatric Rehabilitation'])
    return selected_scenario


def cs_bed_sharing_selection():
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Bed Sharing Option", ['Bed Sharing', 'No Bed Sharing'])
    return bed_sharing_option


def cs_centralize_selection():
    # Display a radio button for centralize selection
    centralizing_option = st.radio("Centralize Option", ['Centralized', 'Decentralized'])
    return centralizing_option


def cs_body_low_respite(bed_sharing_option, centralizing_option):
    container_low_respite = st.container(border=True)

    container_low_respite.subheader('Low complex & respite care')

    container_low_respite.number_input('Number of beds', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of nurses', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of beds 1 nurse can handle', min_value=0, max_value=None, value=8)

    st.write('Bed Sharing Option:', bed_sharing_option)
    st.write('Centralizing Option:', centralizing_option)

    slider_beds = st.slider(
        'Select a range of number of beds',
        0, 100, (25, 75))


def cs_body_high_complex(bed_sharing_option, centralizing_option):
    container_high_complex = st.container(border=True)

    container_high_complex.subheader('High Complex & Geriatric Rehabilitation')

    container_high_complex.number_input('Number of beds', min_value=0, max_value=None, value=10)
    container_high_complex.number_input('Number of therapists', min_value=0, max_value=None, value=12)
    container_high_complex.number_input('Number of beds 1 therapist can handle', min_value=0, max_value=None, value=6)

    # Additional inputs specific to high complex & geriatric rehabilitation
    container_high_complex.checkbox('Specialized Equipment Available')
    container_high_complex.checkbox('24/7 Monitoring')

    st.write('Bed Sharing Option:', bed_sharing_option)
    st.write('Centralizing Option:', centralizing_option)


def plot_low_complex_chart():
    # This function creates an interactive sunburst chart using Plotly
    fig = px.sunburst(names=['Number of Beds', 'Number of Nurses'],
                      parents=['', ''],
                      values=[8, 8],
                      title='Low Complex & Respite Care: Beds and Nurses')

    # Display the chart using st.plotly_chart
    st.plotly_chart(fig)


def plot_high_complex_chart():
    # This function creates an interactive sunburst chart using Plotly
    fig = px.sunburst(names=['Number of Beds', 'Number of Nurses'],
                      parents=['', ''],
                      values=[8, 8],  # Replace with the actual values
                      title='High Complex & Geriatric Rehabiliation: Beds and Nurses')

    # Display the chart using st.plotly_chart
    st.plotly_chart(fig)


def run_simulation(selected_scenario, bed_sharing_option):
    # Perform simulation based on selected_scenario and bed_sharing_option
    st.write('Simulation is running for:', selected_scenario)
    st.write('Bed Sharing Option:', bed_sharing_option)
    # Add simulation logic here


if __name__ == '__main__':
    main_test()