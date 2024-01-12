import streamlit as st
import plotly.express as px

def main():
    cs_sidebar()
    
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
    selected_scenario = st.radio("Select Scenario", ['Low Complex & Respite Care', 'High Complex & Geriatric Rehabilitation'])
    return selected_scenario

def cs_bed_sharing_selection():
    # Display a radio button for bed sharing selection
    bed_sharing_option = st.radio("Bed Sharing Option", ['Bed Sharing', 'No Bed Sharing'])
    return bed_sharing_option

def cs_centralize_selection():
    #Display a radio button for centralize selection
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
                      values=[8,8],
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
    main()

