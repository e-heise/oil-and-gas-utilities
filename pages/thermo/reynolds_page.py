import streamlit as st
import pandas as pd
from calculators.thermo.reynolds_calc import reynolds_number

# set the divider color to be used throughout the page
divider_color = "red"

# title
st.title("Reynolds Number")

# calculation container    
with st.container(border=True):
    density = st.number_input("Density [kg/m3]",
                              min_value=0.0,
                              value=1000.0)
    
    velocity = st.number_input("Velocity [m/s]",
                               min_value=0.0,
                               value=2.5)
    
    diameter = st.number_input("Characteristic Length [m]",
                               min_value=0.0,
                               value=0.05)
    
    viscosity = st.number_input("Dynamic Viscosity [Pa·s]",
                                min_value=0.0,
                                value=1.0e-3,
                                format="%.3e")
    
    if st.button("Calculate", type="primary", width="stretch"):
        try:
            Re = reynolds_number(
                density_kg_m3=density,
                velocity_m_s=velocity,
                diameter_m=diameter,
                dynamic_viscosity_pa_s=viscosity
            )
            
            Re = f"{Re:,.0f}"
            
            st.success(f"Reynolds Number: {Re}")
            
        except ValueError as e:
            st.error(str(e))
    
# useful info expander section            
with st.expander("Useful Info"):
    densities_data = {
        "Fluid": ["Water @ 15°C", "Water @ 50°C", "Air @ 15°C"],
        "Density [kg/m3]": [f"{x:,.2f}" for x in [999.99, 988.00, 1.225]]
    }
    df_densities = pd.DataFrame(densities_data)
    st.subheader("Density of Select Fluids", divider=divider_color)
    st.dataframe(df_densities, hide_index=True, width="content")
    
    st.space()
    
    viscosities_data = {
        "Fluid": ["Water @ 15°C", "Water @ 50°C", "Air @ 20°C"],
        "Dynamic Viscosity [Pa·s]": [f"{x:.3e}" for x in [8.9e-4, 5.44e-4, 1.81e-5]]
    }
    df_viscosities = pd.DataFrame(viscosities_data)
    st.subheader("Dynamic Viscosity of Select Fluids", divider=divider_color)
    st.dataframe(df_viscosities, hide_index=True, width="content")
  
# methodology expander section    
with st.container(border=True):
    st.subheader("Reynolds Number", divider=divider_color)
    st.write("Osborne Reynolds popularized the idea of using the Reynolds number to characterize pipe flows.\n\n "
             "The Reynolds number is defined as: ")

    st.latex(r'''
             Re = \frac{\rho \cdot v \cdot L_c}{\mu}
             '''
             )
    
    st.markdown(
        """
        where:

        - $Re$ is the Reynolds number (dimensionless)
        - $\\rho$ is the fluid density [kg/m³]
        - $v$ is the characteristic velocity [m/s]
        - $L_c$ is the characteristic length [m]
        - $\\mu$ is the dynamic viscosity [Pa·s]\n\n
        """
    )
    
    st.markdown(
    """
    The chosen characteristic length $L_c$ depends on the scenario. In the case
    of pipe flow, $L_c$ is equal to the inner diameter of the pipe.
    
    Chosing an accurate viscosity is important for accuracy of the calculated Reynolds number.
    The "Useful Info" section contains viscosity data for various common fluids.
    """
    )
    
    
    
             