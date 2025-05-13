import streamlit as st
from utils.model import Model


# Create a dictionary for parameters
params = {
    'admissions_per_year': 1000,
    'prop_hasu_using_asu': 0.7,
    'prop_hasu_using_esd_only': 0.1,
    'prop_asu_using_esd': 0.5,
    'los_hasu_mean': 2.0,
    'los_hasu_cv': 1.0,
    'los_asu_no_esd_mean': 15,
    'los_asu_no_esd_cv': 1.0,
    'los_asu_with_esd_mean': 15,
    'los_asu_with_esd_cv': 1.0,
    'los_esd_mean': 20,
    'los_esd_cv': 1.0
}

st.title('Simple stroke system model')

# Add image
st.image('images/system_1.png', caption='Simple Stroke System model', width=600)

# Add a box to enter admissions_per_year
st.sidebar.title("Model parameters")
params['admissions_per_year'] = st.sidebar.number_input('Admissions per year', value=params['admissions_per_year'])
params['prop_hasu_using_asu'] = st.sidebar.number_input('Proportion HASU using ASU', value=params['prop_hasu_using_asu'])
params['prop_hasu_using_esd_only'] = st.sidebar.number_input('Proportion HASU using ESD only', value=params['prop_hasu_using_esd_only'])
params['prop_asu_using_esd'] = st.sidebar.number_input('Proportion ASU using ESD', value=params['prop_asu_using_esd'])
params['los_hasu_mean'] = st.sidebar.number_input('Mean LOS HASU', value=params['los_hasu_mean'])
params['los_hasu_cv'] = st.sidebar.number_input('CV LOS HASU', value=params['los_hasu_cv'])
params['los_asu_no_esd_mean'] = st.sidebar.number_input('Mean LOS ASU no ESD', value=params['los_asu_no_esd_mean'])
params['los_asu_no_esd_cv'] = st.sidebar.number_input('CV LOS ASU no ESD', value=params['los_asu_no_esd_cv'])
params['los_asu_with_esd_mean'] = st.sidebar.number_input('Mean LOS ASU with ESD', value=params['los_asu_with_esd_mean'])
params['los_asu_with_esd_cv'] = st.sidebar.number_input('CV LOS ASU with ESD', value=params['los_asu_with_esd_cv'])
params['los_esd_mean'] = st.sidebar.number_input('Mean LOS ESD', value=params['los_esd_mean'])
params['los_esd_cv'] = st.sidebar.number_input('CV LOS ESD', value=params['los_esd_cv'])


st.subheader('Load and run model')
if st.button('Load and run model'):
    # Load the model with the parameters
    m = Model(params)

    warm_up = 100
    sim_duration = 365 # Duration after warm up
    m.run(warm_up, sim_duration)

    st.image('./output/bed_occupancy.png', caption='Bed Occupancy', use_container_width=True)
    st.write(m.system.audit_report_summary)


