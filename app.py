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

# Add a description

# Add an image
st.image('./images/system_1.png', caption='Flow diagram of the stroke system', width=350)

st.write("""
This is a model that simulates the flow of patients through a simple stroke system:
- HASU: Hyper Acute Stroke Unit
- ASU: Acute Stroke Unit
- ESD: Early Supported Discharge
         

Patients are admitted to the HASU and then may be transferred to the ASU. The model simulates the flow of patients through these components and generates a bed occupancy report and an audit report summary.
- The length of stay (LOS) for each component is defined by a mean (a log-normal distribution with 70% CV is applied to add typical variation in LOS).
- The model parameters can be adjusted using the sidebar.
- The model is run by clicking the "Run model" button (clicking again will simulate another year).
""")

# Add a box to enter admissions_per_year
st.sidebar.title("Model parameters")
params['admissions_per_year'] = st.sidebar.number_input('Admissions per year', value=params['admissions_per_year'], step=50)
params['prop_hasu_using_asu'] = st.sidebar.number_input('Proportion HASU patients using ASU', value=params['prop_hasu_using_asu'], step=0.05)
params['prop_hasu_using_esd_only'] = st.sidebar.number_input('Proportion HASU patients using ESU only', value=params['prop_hasu_using_esd_only'], step=0.05)
params['prop_asu_using_esd'] = st.sidebar.number_input('Proportion ASU patients using ESD', value=params['prop_asu_using_esd'], step=0.05)
params['los_hasu_mean'] = st.sidebar.number_input('Mean LOS (days) in HASU', value=params['los_hasu_mean'], step=0.5)
params['los_asu_no_esd_mean'] = st.sidebar.number_input('Mean LOS (days) in ASU without ESD', value=params['los_asu_no_esd_mean'])
params['los_asu_with_esd_mean'] = st.sidebar.number_input('Mean LOS (days) in ASU with ESD', value=params['los_asu_with_esd_mean'])
params['los_esd_mean'] = st.sidebar.number_input('Mean LOS (days) in ESD', value=params['los_esd_mean'])



if st.button('Run model'):
    # Load the model with the parameters
    m = Model(params)

    warm_up = 100
    sim_duration = 365 # Duration after warm up
    m.run(warm_up, sim_duration)

    # Create 2 columns for the outputs
    col1, col2 = st.columns(2)

    with col1:
        st.image('./output/bed_occupancy.png', caption='Bed Occupancy', use_container_width=True)
    with col2:
        st.write(m.system.audit_report_summary)


