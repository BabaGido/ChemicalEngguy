import math
import streamlit as st

# Constants
DENSITY_CARBON_STEEL = 490  # lb/ft^3
WALL_THICKNESS = 0.20833  # 2.5 inches in feet

# Material factors for vessels (from Table 22.26)
MATERIAL_FACTORS = {
    "carbon steel": {"F_M": 1.0, "density": 490},  # lb/ft^3
    "low-alloy steel": {"F_M": 1.2, "density": 490},
    "stainless steel 304": {"F_M": 1.7, "density": 500},
    "stainless steel 316": {"F_M": 2.1, "density": 500},
    "carpenter 20cb-3": {"F_M": 3.2, "density": 500},
    "nickel-200": {"F_M": 5.4, "density": 555},
    "monel-400": {"F_M": 3.6, "density": 555},
    "inconel-600": {"F_M": 3.9, "density": 555},
    "incoloy-825": {"F_M": 3.7, "density": 555},
    "titanium": {"F_M": 7.7, "density": 280},
}

# Tray type factors
TRAY_TYPE_FACTORS = {
    "sieve": 1.0,
    "valve": 1.18,
}

# Tray material factors
TRAY_MATERIAL_FACTORS = {
    "carbon steel": 1.0,
    "stainless steel": 1.4,
}

# Heat exchanger material factors (from Table 22.25)
HEAT_EXCHANGER_MATERIAL_FACTORS = {
    "carbon steel/carbon steel": {"a": 0.00, "b": 0.09},
    "carbon steel/brass": {"a": 1.08, "b": 0.05},
    "carbon steel/stainless steel": {"a": 1.75, "b": 0.13},
    "carbon steel/monel": {"a": 2.7, "b": 0.13},
    "carbon steel/titanium": {"a": 3.2, "b": 0.16},
    "carbon steel/cr-mo steel": {"a": 1.55, "b": 0.05},
    "cr-mo steel/cr-mo steel": {"a": 1.70, "b": 0.07},
    "stainless steel/stainless steel": {"a": 2.70, "b": 0.07},
    "monel/monel": {"a": 3.3, "b": 0.08},
    "titanium/titanium": {"a": 9.6, "b": 0.06},
}

# Compressor material factors
COMPRESSOR_MATERIAL_FACTORS = {
    "carbon steel": 1.0,
    "stainless steel": 2.5,
    "nickel alloy": 5.0,
}

def calculate_vessel_weight(diameter, length, density):
    """
    Calculate the weight of the vessel.
    Equation: W = π (D_i + t)(L + 0.8D_i) t ρ
    """
    weight = (
        math.pi
        * (diameter + WALL_THICKNESS)
        * (length + 0.8 * diameter)
        * WALL_THICKNESS
        * density
    )
    return weight

def calculate_vessel_cost(weight, equipment_type):
    """
    Calculate the base cost of the vessel.
    Equation for Reactor: C_V = exp(7.0132 + 0.18255 * ln(W) + 0.02297 * (ln(W))^2)
    Equation for Distillation Column: C_V = exp(7.2756 + 0.18255 * ln(W) + 0.02297 * (ln(W))^2)
    """
    ln_weight = math.log(weight)
    if equipment_type == "reactor":
        vessel_cost = math.exp(7.0132 + 0.18255 * ln_weight + 0.02297 * (ln_weight**2))
    elif equipment_type == "distillation column":
        vessel_cost = math.exp(7.2756 + 0.18255 * ln_weight + 0.02297 * (ln_weight**2))
    return vessel_cost

def calculate_platform_ladder_cost(diameter, length, equipment_type):
    """
    Calculate the cost of platforms and ladders.
    Equation for Reactor: C_PL = 361.8 * D^0.73960 * L^0.70684
    Equation for Distillation Column: C_PL = 300.9 * D^0.63316 * L^0.80161
    """
    if equipment_type == "reactor":
        platform_ladder_cost = 361.8 * (diameter**0.73960) * (length**0.70684)
    elif equipment_type == "distillation column":
        platform_ladder_cost = 300.9 * (diameter**0.63316) * (length**0.80161)
    return platform_ladder_cost

def calculate_tray_cost(diameter, num_trays, tray_type, tray_material):
    """
    Calculate the cost of trays.
    Equation: C_T = N_T * F_NT * F_TT * F_TM * C_BT
    C_BT = 468 * exp(0.1739 * D)  (for sieve trays)
    """
    # Base tray cost
    base_tray_cost = 468 * math.exp(0.1739 * diameter)

    # Tray type factor (F_TT)
    tray_type_factor = TRAY_TYPE_FACTORS.get(tray_type, 1.0)

    # Number of trays factor (F_NT)
    if num_trays > 20:
        num_trays_factor = 1.0
    else:
        num_trays_factor = 2.25 / (1.0414**num_trays)

    # Material factor for trays (F_TM)
    tray_material_factor = TRAY_MATERIAL_FACTORS.get(tray_material, 1.0)

    # Total tray cost
    tray_cost = num_trays * num_trays_factor * tray_type_factor * tray_material_factor * base_tray_cost
    return tray_cost

def calculate_reactor_cost():
    """
    Calculate the total cost of a reactor.
    """
    st.subheader("Reactor Cost Calculation")

    # Inputs
    space_time = st.number_input("Enter the space time (τ) in minutes (or 0 to skip): ", min_value=0.0)
    volumetric_flow_rate = st.number_input("Enter the volumetric flow rate (Q) in ft³/min (or 0 to skip): ", min_value=0.0)

    if space_time and volumetric_flow_rate:
        # Calculate dimensions using space time and volumetric flow rate
        volume = volumetric_flow_rate * space_time
        diameter = (4 * volume / (2.5 * math.pi)) ** (1 / 3)
        length = 2.5 * diameter
        st.write(f"Calculated diameter: {diameter:.2f} ft")
        st.write(f"Calculated length: {length:.2f} ft")
    else:
        # Ask for dimensions directly
        diameter = st.number_input("Enter the diameter of the reactor (ft): ", min_value=0.0)
        length = st.number_input("Enter the length of the reactor (ft): ", min_value=0.0)

    material = st.selectbox("Enter the material of construction:", list(MATERIAL_FACTORS.keys()))
    material_data = MATERIAL_FACTORS.get(material, {"F_M": 1.0, "density": 490})
    density = material_data["density"]
    material_factor = material_data["F_M"]

    # Calculate vessel weight
    weight = calculate_vessel_weight(diameter, length, density)
    st.write(f"Vessel weight (W): {weight:.2f} lbs")

    # Calculate vessel cost
    vessel_cost = calculate_vessel_cost(weight, "reactor")
    st.write(f"Base vessel cost (C_V): ${vessel_cost:.2f}")

    # Apply material factor for vessel
    vessel_cost *= material_factor
    st.write(f"Adjusted vessel cost (C_PV = F_M * C_V): ${vessel_cost:.2f}")

    # Calculate platform and ladder cost
    platform_ladder_cost = calculate_platform_ladder_cost(diameter, length, "reactor")
    st.write(f"Platform and ladder cost (C_PL): ${platform_ladder_cost:.2f}")

    # Total cost
    total_cost = vessel_cost + platform_ladder_cost
    st.success(f"Total Reactor Cost: ${total_cost:,.2f}")

def calculate_distillation_column_cost():
    """
    Calculate the total cost of a distillation column.
    """
    st.subheader("Distillation Column Cost Calculation")

    # Inputs
    diameter = st.number_input("Enter the diameter of the column (ft): ", min_value=0.0)
    length = st.number_input("Enter the length of the column (ft): ", min_value=0.0)
    num_trays = st.number_input("Enter the number of trays: ", min_value=0)
    material = st.selectbox("Enter the material of construction:", list(MATERIAL_FACTORS.keys()))
    tray_type = st.selectbox("Enter the tray type:", list(TRAY_TYPE_FACTORS.keys()))
    tray_material = st.selectbox("Enter the tray material:", list(TRAY_MATERIAL_FACTORS.keys()))

    material_data = MATERIAL_FACTORS.get(material, {"F_M": 1.0, "density": 490})
    density = material_data["density"]
    material_factor = material_data["F_M"]

    # Calculate vessel weight
    weight = calculate_vessel_weight(diameter, length, density)
    st.write(f"Vessel weight (W): {weight:.2f} lbs")

    # Calculate vessel cost
    vessel_cost = calculate_vessel_cost(weight, "distillation column")
    st.write(f"Base vessel cost (C_V): ${vessel_cost:.2f}")

    # Apply material factor for vessel
    vessel_cost *= material_factor
    st.write(f"Adjusted vessel cost (C_PV = F_M * C_V): ${vessel_cost:.2f}")

    # Calculate platform and ladder cost
    platform_ladder_cost = calculate_platform_ladder_cost(diameter, length, "distillation column")
    st.write(f"Platform and ladder cost (C_PL): ${platform_ladder_cost:.2f}")

    # Calculate tray cost
    tray_cost = calculate_tray_cost(diameter, num_trays, tray_type, tray_material)
    st.write(f"Tray cost (C_T): ${tray_cost:.2f}")

    # Total cost
    total_cost = vessel_cost + platform_ladder_cost + tray_cost
    st.success(f"Total Distillation Column Cost: ${total_cost:,.2f}")

def calculate_heat_exchanger_cost():
    """
    Calculate the total cost of a shell-and-tube heat exchanger.
    """
    st.subheader("Shell-and-Tube Heat Exchanger Cost Calculation")

    # Inputs
    heat_duty = st.number_input("Enter the heat duty (Q) in Btu/hr: ", min_value=0.0)
    flux_rate = st.number_input("Enter the heat exchange flux rate (Btu/hr-ft²): ", min_value=0.0)
    area = heat_duty / flux_rate
    st.write(f"Calculated heat exchange area (A): {area:.2f} ft²")

    pressure = st.number_input("Enter the design pressure (psig): ", min_value=0.0)
    material = st.selectbox("Enter the materials of construction:", list(HEAT_EXCHANGER_MATERIAL_FACTORS.keys()))
    tube_length = st.number_input("Enter the tube length (ft): ", min_value=0.0)

    # Calculate base cost (C_B)
    ln_area = math.log(area)
    base_cost = math.exp(11.667 - 0.8709 * ln_area + 0.09005 * (ln_area**2))
    st.write(f"Base cost (C_B): ${base_cost:.2f}")

    # Pressure correction factor (F_P)
    if pressure > 100:
        pressure_factor = 0.9803 + 0.018 * (pressure / 100) + 0.0017 * (pressure / 100)**2
    else:
        pressure_factor = 1.0
    st.write(f"Pressure correction factor (F_P): {pressure_factor:.2f}")

    # Tube length correction factor (F_L)
    if tube_length < 20:
        tube_length_factor = 1.0  # Assume F_L = 1 for tube lengths < 20 ft
    else:
        tube_length_factor = 1.0
    st.write(f"Tube length correction factor (F_L): {tube_length_factor:.2f}")

    # Material correction factor (F_M)
    material_data = HEAT_EXCHANGER_MATERIAL_FACTORS.get(material, {"a": 0.00, "b": 0.09})
    material_factor = material_data["a"] + (area / 100) ** material_data["b"]
    st.write(f"Material correction factor (F_M): {material_factor:.2f}")

    # Total cost
    total_cost = pressure_factor * material_factor * tube_length_factor * base_cost
    st.success(f"Total Heat Exchanger Cost: ${total_cost:,.2f}")

def calculate_compressor_cost():
    """
    Calculate the total cost of a compressor.
    """
    st.subheader("Compressor Cost Calculation")

    # Inputs
    inlet_flow = st.number_input("Enter the inlet flow rate (Q₁) in ft³/min: ", min_value=0.0)
    inlet_pressure = st.number_input("Enter the inlet pressure (P₁) in psi: ", min_value=0.0)
    outlet_pressure = st.number_input("Enter the outlet pressure (P₂) in psi: ", min_value=0.0)
    specific_heat_ratio = st.number_input("Enter the ratio of specific heats (k = C_p/C_v): ", min_value=0.0)
    efficiency = st.number_input("Enter the overall efficiency (η) as a decimal (e.g., 0.78): ", min_value=0.0, max_value=1.0)
    drive_type = st.selectbox("Enter the drive type:", ["electric", "steam turbine", "gas turbine"])
    material = st.selectbox("Enter the material of construction:", list(COMPRESSOR_MATERIAL_FACTORS.keys()))

    # Calculate power consumption (P_c)
    power_consumption = 0.00436 * (specific_heat_ratio / (specific_heat_ratio - 1)) * (inlet_flow * inlet_pressure / efficiency) * ((outlet_pressure / inlet_pressure) ** ((specific_heat_ratio - 1) / specific_heat_ratio) - 1)
    st.write(f"Power consumption (P_c): {power_consumption:.2f} horsepower")

    # Calculate base cost (C_B)
    base_cost = math.exp(7.580 + 0.8 * math.log(power_consumption))
    st.write(f"Base cost (C_B): ${base_cost:.2f}")

    # Drive type factor (F_D)
    drive_factors = {
        "electric": 1.0,
        "steam turbine": 1.15,
        "gas turbine": 1.25,
    }
    drive_factor = drive_factors.get(drive_type, 1.0)
    st.write(f"Drive type factor (F_D): {drive_factor:.2f}")

    # Material factor (F_M)
    material_factor = COMPRESSOR_MATERIAL_FACTORS.get(material, 1.0)
    st.write(f"Material factor (F_M): {material_factor:.2f}")

    # Total cost
    total_cost = drive_factor * material_factor * base_cost
    st.success(f"Total Compressor Cost: ${total_cost:,.2f}")

def main():
    st.title("Equipment Cost Calculator")
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Select the equipment to calculate the cost for:", ["Reactor", "Distillation Column", "Shell-and-Tube Heat Exchanger", "Compressor"])

    if choice == "Reactor":
        calculate_reactor_cost()
    elif choice == "Distillation Column":
        calculate_distillation_column_cost()
    elif choice == "Shell-and-Tube Heat Exchanger":
        calculate_heat_exchanger_cost()
    elif choice == "Compressor":
        calculate_compressor_cost()

if __name__ == "__main__":
    main()