import streamlit as st

# Title of the app
st.title("Utilities Calculator for Ethylbenzene Production")

# Navigation bar for selecting the calculation
st.sidebar.header("Navigation")
calculation_type = st.sidebar.radio(
    "Select the utility to calculate:",
    ["Cooling Water", "Natural Gas", "CO₂ Emissions"]
)

# Constants (hidden in the background)
Cp_water = 1.0  # Specific heat capacity of water (kcal/kg·°C)
delta_H_comb = 13277.0  # Heat of combustion for natural gas (kcal/kg)
CO2_emission_factor = 2.74  # kg CO₂ per kg of natural gas burned
efficiency = 0.8  # Efficiency of the fired heater

# Function to calculate cooling water
def calculate_cooling_water(Q_cooling, Cp_water, delta_T_cw):
    m_cw = Q_cooling / (Cp_water * delta_T_cw)  # Mass flow rate of cooling water (kg/hr)
    return m_cw

# Function to calculate natural gas
def calculate_natural_gas(Q_heating, delta_H_comb, efficiency):
    Q_heater = Q_heating / efficiency  # Heat required by the fired heater (kcal/hr)
    m_ng = Q_heater / delta_H_comb  # Mass flow rate of natural gas (kg/hr)
    return Q_heater, m_ng

# Function to calculate CO₂ emissions
def calculate_CO2_emissions(m_ng, CO2_emission_factor):
    m_CO2 = m_ng * CO2_emission_factor  # Mass flow rate of CO₂ (kg/hr)
    return m_CO2

# Display inputs and results based on the selected calculation
if calculation_type == "Cooling Water":
    st.header("Cooling Water Calculation")
    Q_cooling = st.number_input("Heat removed by cooling water (kcal/hr)", value=8621900.0)
    delta_T_cw = st.number_input("Temperature difference for cooling water (°C)", value=16.0)
    
    if st.button("Calculate Cooling Water"):
        m_cw = calculate_cooling_water(Q_cooling, Cp_water, delta_T_cw)
        st.success(f"Mass flow rate of cooling water (m_cw): **{m_cw:.2f} kg/hr**")

elif calculation_type == "Natural Gas":
    st.header("Natural Gas Calculation")
    Q_heating = st.number_input("Heat added by steam (kcal/hr)", value=7194400.0)
    
    if st.button("Calculate Natural Gas"):
        Q_heater, m_ng = calculate_natural_gas(Q_heating, delta_H_comb, efficiency)
        st.success(f"Heat required by the fired heater (Q_heater): **{Q_heater:.2f} kcal/hr**")
        st.success(f"Mass flow rate of natural gas (m_ng): **{m_ng:.2f} kg/hr**")

elif calculation_type == "CO₂ Emissions":
    st.header("CO₂ Emissions Calculation")
    m_ng = st.number_input("Mass flow rate of natural gas (kg/hr)", value=677.43)
    
    if st.button("Calculate CO₂ Emissions"):
        m_CO2 = calculate_CO2_emissions(m_ng, CO2_emission_factor)
        st.success(f"Mass flow rate of CO₂ emissions (m_CO2): **{m_CO2:.2f} kg/hr**")
