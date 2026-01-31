import streamlit as st

from calculators.utilities.barometric_pressure_calc import barometric_pressure

st.title("Barometric Pressure")

with st.container(border=True):
    altitude = st.number_input("Altitude [m]",
                               min_value=0.0,
                               value=1045.0)
    
if st.button("Calculate", type="primary", width="stretch"):
    try:
        Patm = barometric_pressure(
        altitude_m=altitude)
        
        Patm = f"{Patm:.2f} kPa"

        st.success(f"Barometric Pressure: {Patm}")

    except ValueError as e:
        st.error(str(e))

with st.container(border=True):
    st.subheader("Barometric Pressure Formula")

    st.markdown("""
                The U.S. Standard Atmosphere provides two formulas for calculation the barometric pressure as a function of altitude. 
                The second formula, which assumes no variation of temperature with altitude, is used here:
                """)
    
    st.latex(r"""
             P = P_b \cdot \exp\left(\frac{-g_0^{'} M_0 (H - H_b)}{R^{*} T_{M,b}}\right)
             """)
    
    st.markdown("""
                where:
                
                - $P$ is the barometric pressure at altitude [Pa]
                - $P_b$ is the reference pressure = 101,325 kPa
                - $g_0^{'}$ is the acceleration due to gravity = 9.80665 m/s
                - $M_0$ is the mean molecular weight of air at sea level = 28.9644 kg/kmol
                - $H$ is the altitude at which to calculate the barometric pressure [m]
                - $H_b$ is the reference altitude = 0.0 m (sea level)
                - $R^{*}$ is the ideal gas constant = 8314.32 J/kmol/K
                - $T_{M,b}$ is the reference temperature = 288.15 K
                """)