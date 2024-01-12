import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


def main():
    cs_sidebar()
    
    # Get the selected scenario
    selected_scenario = cs_scenario_selection()

    # Get the selected bed sharing option
    bed_sharing_option = cs_bed_sharing_selection()

    if selected_scenario == 'Low Complex & Respite Care':
        cs_body_low_respite(bed_sharing_option)
        plot_low_complex_chart()
    elif selected_scenario == 'High Complex & Geriatric Rehabilitation':
        cs_body_high_complex(bed_sharing_option)
        plot_high_complex_chart()

        # Add a button to run the simulation
    if st.button("Run Simulation"):
        run_simulation(selected_scenario, bed_sharing_option)


def cs_sidebar():
    with st.sidebar:
        st.write('**Low complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate GP')
            st.write('Outflow home rate')
            st.write('outflow home with adjustments rate')
            st.write('Outflow long term care rate')
            st.write('outflow geriatric care rate')
            st.write('Outflow hospice rate')
            st.write('outflow death rate')
        with col2:
            st.number_input('rate GP for low complex', min_value=0.0, max_value=None, value=1.34, label_visibility='collapsed')
            st.number_input("home rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.7, label_visibility='collapsed')
            st.number_input("home with adjustments rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.14, label_visibility='collapsed')
            st.number_input("Outflow long term care rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.1, label_visibility='collapsed')
            st.number_input("outflow geriatric care rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.02, label_visibility='collapsed')
            st.number_input("Outflow hospice rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.02, label_visibility='collapsed')
            st.number_input("Outflow death rate for low complex", min_value=0.0, max_value=1.0,
                        value=0.02, label_visibility='collapsed')

        st.write('**Respite care**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate')
            st.write('Outflow home rate')
            st.write('outflow home with adjustments rate')
            st.write('Outflow long term care rate')
            st.write('outflow geriatric care rate')
            st.write('Outflow hospice rate')
            st.write('outflow death rate')
        with col2:
            st.number_input("rate GP respite", min_value=0.0, max_value=1.0, value=0.57,
                            label_visibility='collapsed')
            st.number_input("home rate respite", min_value=0.0, max_value=1.0,
                            value=0.9, label_visibility='collapsed')
            st.number_input("home with adjustments rate respite", min_value=0.0, max_value=1.0,
                            value=0.05, label_visibility='collapsed')
            st.number_input("Outflow long term care rate respite", min_value=0.0, max_value=1.0,
                            value=0.03, label_visibility='collapsed')
            st.number_input("outflow geriatric care rate respite", min_value=0.0, max_value=1.0,
                            value=0.01, label_visibility='collapsed')
            st.number_input("Outflow hospice rate respite", min_value=0.0, max_value=1.0,
                            value=0.005, label_visibility='collapsed')
            st.number_input("Outflow death rate respite", min_value=0.0, max_value=1.0,
                            value=0.005, label_visibility='collapsed')

        st.write('**High complex**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate GP')
            st.write('Arrival rate Emergency Department')
            st.write('Arrival rate Hospital')
            st.write('Outflow home rate')
            st.write('outflow home with adjustments rate')
            st.write('Outflow long term care rate')
            st.write('outflow geriatric care rate')
            st.write('Outflow hospice rate')
            st.write('outflow death rate')
        with col2:
            st.number_input("rate GP high", min_value=0.0, max_value=None, value=1.34,
                            label_visibility='collapsed')
            st.number_input("rate ED high", min_value=0.0, max_value=None, value=0.83,
                            label_visibility='collapsed')
            st.number_input("rate hospital high", min_value=0.0, max_value=None, value=0.94,
                            label_visibility='collapsed')
            st.number_input("home rate respite", min_value=0.0, max_value=1.0,
                            value=0.578, label_visibility='collapsed')
            st.number_input("home with adjustments rate respite", min_value=0.0, max_value=1.0,
                            value=0.107, label_visibility='collapsed')
            st.number_input("Outflow long term care rate respite", min_value=0.0, max_value=1.0,
                            value=0.198, label_visibility='collapsed')
            st.number_input("outflow geriatric care rate respite", min_value=0.0, max_value=1.0,
                            value=0.034, label_visibility='collapsed')
            st.number_input("Outflow hospice rate respite", min_value=0.0, max_value=1.0,
                            value=0.023, label_visibility='collapsed')
            st.number_input("Outflow death rate respite", min_value=0.0, max_value=1.0,
                            value=0.06, label_visibility='collapsed')

        st.write('**Geriatric rehabilitation**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('Arrival rate hospital')
            st.write('Outflow home rate')
            st.write('outflow home with adjustments rate')
            st.write('Outflow long term care rate')
            st.write('outflow geriatric care rate')
            st.write('Outflow hospice rate')
            st.write('outflow death rate')
        with col2:
            st.number_input("rate hospital Geriatric", min_value=0.0, max_value=None, value=0.54,
                            label_visibility='collapsed')
            st.number_input("home rate Geriatric", min_value=0.0, max_value=1.0,
                            value=0.6, label_visibility='collapsed')
            st.number_input("home with adjustments rate Geriatric", min_value=0.0, max_value=1.0,
                            value=0.107, label_visibility='collapsed')
            st.number_input("Outflow long term care rate Geriatric", min_value=0.0, max_value=1.0,
                            value=0.21, label_visibility='collapsed')
            st.number_input("outflow geriatric care rate Geriatric", min_value=0.0, max_value=0.0,
                            value=0.0, label_visibility='collapsed') # not possible
            st.number_input("Outflow hospice rate Geriatric", min_value=0.0, max_value=1.0,
                            value=0.023, label_visibility='collapsed')
            st.number_input("Outflow death rate Geriatric", min_value=0.0, max_value=1.0,
                            value=0.06, label_visibility='collapsed')

def cs_scenario_selection():
    # Display a radio button for scenario selection
    selected_scenario = st.radio("Select Scenario", ['Low Complex & Respite Care', 'High Complex & Geriatric Rehabilitation'])
    return selected_scenario

def cs_bed_sharing_selection():
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Bed Sharing Option", ['Bed Sharing', 'No Bed Sharing'])
    return bed_sharing_option

def cs_body_low_respite(bed_sharing_option):
    container_low_respite = st.container(border=True)

    container_low_respite.subheader('Low complex & respite care')

    container_low_respite.number_input('Number of beds', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of nurses', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of beds 1 nurse can handle', min_value=0, max_value=None, value=8)

    st.write('Bed Sharing Option:', bed_sharing_option)

    slider_beds = st.slider(
        'Select a range of number of beds',
        0, 100, (25, 75))

def cs_body_high_complex(bed_sharing_option):
    container_high_complex = st.container(border=True)

    container_high_complex.subheader('High Complex & Geriatric Rehabilitation')

    container_high_complex.number_input('Number of beds', min_value=0, max_value=None, value=10)
    container_high_complex.number_input('Number of therapists', min_value=0, max_value=None, value=12)
    container_high_complex.number_input('Number of beds 1 therapist can handle', min_value=0, max_value=None, value=6)

    # Additional inputs specific to high complex & geriatric rehabilitation
    container_high_complex.checkbox('Specialized Equipment Available')
    container_high_complex.checkbox('24/7 Monitoring')

    st.write('Bed Sharing Option:', bed_sharing_option)

    # Other input components related to high complex care can be added as needed


def plot_low_complex_chart():
    # This function creates an interactive sunburst chart using Plotly
    fig = px.sunburst(names=['Number of Beds', 'Number of Nurses'],
                      parents=['', ''],
                      values=[8, 8],  # Replace with the actual values
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
    # Your simulation logic goes here
    st.write(f"Running simulation for scenario: {selected_scenario}")
    st.write(f"Bed Sharing Option: {bed_sharing_option}")
    # Add your simulation code here

if __name__ == '__main__':
    main()

