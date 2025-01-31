import streamlit as st

# Title of the app
st.title("Utility Calculator for Ethylbenzene Production")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

# Cooling Water Inputs
st.sidebar.subheader("Cooling Water")
Q_cooling = st.sidebar.number_input("Heat removed by cooling water (kcal/hr)", value=8621900.0)
Cp_water = st.sidebar.number_input("Specific heat capacity of water (kcal/kg·°C)", value=1.0)
delta_T_cw = st.sidebar.number_input("Temperature difference for cooling water (°C)", value=16.0)

# Natural Gas Inputs
st.sidebar.subheader("Natural Gas")
Q_heating = st.sidebar.number_input("Heat added by steam (kcal/hr)", value=7194400.0)
delta_H_comb = st.sidebar.number_input("Heat of combustion for natural gas (kcal/kg)", value=13277.0)
efficiency = st.sidebar.number_input("Efficiency of the fired heater (as a decimal)", value=0.8)
CO2_emission_factor = st.sidebar.number_input("CO₂ emission factor (kg CO₂/kg natural gas)", value=2.74)

# Calculations
def calculate_cooling_water(Q_cooling, Cp_water, delta_T_cw):
    m_cw = Q_cooling / (Cp_water * delta_T_cw)  # Mass flow rate of cooling water (kg/hr)
    return m_cw

def calculate_natural_gas(Q_heating, delta_H_comb, efficiency):
    Q_heater = Q_heating / efficiency  # Heat required by the fired heater (kcal/hr)
    m_ng = Q_heater / delta_H_comb  # Mass flow rate of natural gas (kg/hr)
    return Q_heater, m_ng

def calculate_CO2_emissions(m_ng, CO2_emission_factor):
    m_CO2 = m_ng * CO2_emission_factor  # Mass flow rate of CO₂ (kg/hr)
    return m_CO2

# Perform calculations
m_cw = calculate_cooling_water(Q_cooling, Cp_water, delta_T_cw)
Q_heater, m_ng = calculate_natural_gas(Q_heating, delta_H_comb, efficiency)
m_CO2 = calculate_CO2_emissions(m_ng, CO2_emission_factor)

# Display results
st.header("Results")

st.subheader("Cooling Water")
st.write(f"Mass flow rate of cooling water (m_cw): **{m_cw:.2f} kg/hr**")

st.subheader("Natural Gas")
st.write(f"Heat required by the fired heater (Q_heater): **{Q_heater:.2f} kcal/hr**")
st.write(f"Mass flow rate of natural gas (m_ng): **{m_ng:.2f} kg/hr**")

st.subheader("CO₂ Emissions")
st.write(f"Mass flow rate of CO₂ emissions (m_CO2): **{m_CO2:.2f} kg/hr**")

# Intermediate Values
st.header("Intermediate Values")
st.write(f"Heat removed by cooling water (Q_cooling): **{Q_cooling:.2f} kcal/hr**")
st.write(f"Specific heat capacity of water (Cp_water): **{Cp_water} kcal/kg·°C**")
st.write(f"Temperature difference for cooling water (ΔT_cw): **{delta_T_cw} °C**")
st.write(f"Heat added by steam (Q_heating): **{Q_heating:.2f} kcal/hr**")
st.write(f"Heat of combustion for natural gas (ΔH_comb): **{delta_H_comb} kcal/kg**")
st.write(f"Efficiency of the fired heater: **{efficiency * 100}%**")
st.write(f"CO₂ emission factor: **{CO2_emission_factor} kg CO₂/kg natural gas**")