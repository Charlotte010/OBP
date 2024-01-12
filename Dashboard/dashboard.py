import streamlit as st
import pandas as pd
#
# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = 'collapsed'

st.set_page_config(
    # page_title='page1',
    # page_icon='📋',
    layout='wide',
    initial_sidebar_state='collapsed' #st.session_state.sidebar_state #'collapsed'
)

def main():
    cs_sidebar()
    cs_body()

    return None



st.title('Predicting waiting times Short  ...')
st.write('Welcome, in this app...')


def cs_sidebar():
    ###################
    # side bar info. Parameters that are not frequently adjusted
    ###################

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
    # st.number_input('Arrival rate GP for low complex', min_value=0.0, max_value=None, value=1.34)
    # st.number_input('Arrival rate GP for respite care', min_value=0.0, max_value=None, value=0.57)
    #
    # st.number_input('Outflow home rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.7)
    # st.number_input('outflow home with adjustments rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.14)
    # st.number_input('Outflow long term care rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.1)
    # st.number_input('outflow geriatric care rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.02)
    # st.number_input('Outflow hospice rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.02)
    # st.number_input('outflow death rate for low complex', min_value=0.0, max_value=None,
    #                 value=0.02)

##########################
# Main body
##########################

def cs_body():
    container_low_respite = st.container(border=True)

    container_low_respite.subheader('Low complex & respite care')

    container_low_respite.number_input('Number of beds', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of nurses', min_value=0, max_value=None, value=8)
    container_low_respite.number_input('Number of beds 1 nurse can handle', min_value=0, max_value=None, value=8)

    # if st.button('Click here to change other parameters'):
    #     st.session_state.sidebar_state = 'expanded' if st.session_state.sidebar_state == 'collapsed' else 'collapsed'
    #     # Force an app rerun after switching the sidebar state.
    #     st.experimental_rerun()

# container_arrivals = st.container(border=True)
# container_arrivals.subheader('Low complex & respite care')
# container_arrivals.latex(r"""
#     \text{The arrival rates are given by } \lambda{ij}""")


    #voor later
    st.write('testing')
    slider_beds = st.slider(
        'Select a range of number of beds',
        0, 100, (25, 75))

# st.write(test, slider_beds)

if __name__ == '__main__':
    main()