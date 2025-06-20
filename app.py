# To run this app, use the command:
# streamlit run app.py

import streamlit as st
from utils.model import Model


# Create a dictionary for parameters
params = {
    'admissions_per_year': 1000,
    'prop_hasu_using_asu': 0.7,
    'prop_hasu_using_esd_only': 0.1,
    'prop_asu_using_esd': 0.5,
    'los_hasu_mean': 2.0,
    'los_hasu_cv': 0.7,
    'los_asu_no_esd_mean': 28,
    'los_asu_no_esd_cv': 0.7,
    'los_asu_with_esd_mean': 21,
    'los_asu_with_esd_cv': 0.7,
    'los_esd_mean': 20,
    'los_esd_cv': 0.7
}

st.title('Simple stroke system model')

# Add a sidebar to enter parameters
st.sidebar.title("Model parameters")
params['admissions_per_year'] = st.sidebar.number_input('Admissions per year', value=params['admissions_per_year'], step=50)
params['prop_hasu_using_asu'] = st.sidebar.number_input('Proportion HASU patients using ASU (with or without ESD)', value=params['prop_hasu_using_asu'], step=0.05)
params['prop_hasu_using_esd_only'] = st.sidebar.number_input('Proportion HASU patients using ESU only (no ASU use)', value=params['prop_hasu_using_esd_only'], step=0.05)
params['prop_asu_using_esd'] = st.sidebar.number_input('Proportion ASU patients using ESD', value=params['prop_asu_using_esd'], step=0.05)
params['los_hasu_mean'] = st.sidebar.number_input('Mean LoS (days) in HASU', value=params['los_hasu_mean'], step=0.5)
params['los_asu_no_esd_mean'] = st.sidebar.number_input('Mean LoS (days) in ASU without ESD', value=params['los_asu_no_esd_mean'])
params['los_asu_with_esd_mean'] = st.sidebar.number_input('Mean LoS (days) in ASU with ESD', value=params['los_asu_with_esd_mean'])
params['los_esd_mean'] = st.sidebar.number_input('Mean LoS (days) in ESD', value=params['los_esd_mean'])

# Add a description

col_1, col_2 = st.columns(2, gap="large")

with col_1:

    # Add an image
    st.image('./images/system_1.png', caption='Flow diagram of the stroke system', width=350)

    st.write("""
    This is a model that simulates the flow of patients through a simple stroke system:
    - HASU: Hyper Acute Stroke Unit
    - ASU: Acute Stroke Unit (may also be known as inpatient rehab)
    - ESD: Early Supported Discharge
            

    Patients are admitted to the HASU and then may be transferred to the ASU. The model simulates the flow of patients through HASU, ASU and ESD.
    - The length of stay (LOS) for each component is defined by a mean (a log-normal distribution with 70% CV is applied to add typical variation in LOS).
    """)

with col_2:

    st.write("""To run the model, adjust parameters in the sidebar, and click 'Run Model' (clicking again will simulate another year).  
        """)

    if st.button('Run model', use_container_width=True):
        # Load the model with the parameters
        m = Model(params)

        warm_up = 100
        sim_duration = 365 # Duration after warm up
        m.run(warm_up, sim_duration)

        st.write("""The chart below shows bed occupancy in HASU and ASU over a year if beds were 
                 always available. The coloured blocks show the range of occupancy numbers that will 
                 cover 90% of bed requirements
                 """)

        st.image('./output/bed_occupancy.png', caption='Bed Occupancy', use_container_width=True)

        st.write("""The table below describes bed or ESD occupancy if beds/ESD were always available.
                 """)

        st.write(m.system.audit_report_summary)