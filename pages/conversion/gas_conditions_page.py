import streamlit as st

from calculators.conversion.gas_conditions_calc import gas_conditions_converter

divider_color = "red"

if "state_z_factor_calc" not in st.session_state:
    st.session_state.state_z_factor_calc = False

st.title("Gas Flow Rate Converter")

with st.container(border=True):    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("State #1 Conditions")
        pressure1 = st.number_input("Pressure 1 [kPa]",
                        min_value=-101.325,
                        value=1034.0)
        
        temperature1 = st.number_input("Temperature 1 [°C]",
                                       min_value=-273.15,
                                       value=15.0)

        compressibility1 = st.number_input("Compressibility 1",
                                           min_value=0.0,
                                           value=0.95,
                                           disabled=st.session_state.state_z_factor_calc)
        
        volume1 = st.number_input("Volume 1 [m3]",
                                  min_value=0.0,
                                  value=1.0)
        
        st.checkbox("Use GPSA Z-Factor Correlation?",
                    key="state_z_factor_calc")
        
        specific_gravity = st.number_input("Specific Gravity Relative to Air",
                                       min_value=0.0,
                                       value=0.600,
                                       disabled=not(st.session_state.state_z_factor_calc))
        
        
    with col2:
        st.subheader("State #2 Conditions")
        pressure2 = st.number_input("Pressure 2 [kPa]",
                        min_value=-101.325,
                        value=1034.0)
        
        temperature2 = st.number_input("Temperature 2 [°C]",
                                       min_value=-273.15,
                                       value=15.0)

        compressibility2 = st.number_input("Compressibility 2",
                                           min_value=0.0,
                                           value=0.95,
                                           disabled=st.session_state.state_z_factor_calc)        
        
if st.button("Calculate", type="primary", width="stretch"):
        try:
            V2 = gas_conditions_converter(
                pressure1_Pa=pressure1*1000,
                temperature1_K=temperature1+273.15,
                compressibility1=compressibility1,
                volume1_m3=volume1,
                pressure2_Pa=pressure2*1000,
                temperature2_K=temperature2+273.15,
                compressibility2=compressibility2,
                calc_z_factor=st.session_state.state_z_factor_calc,
                specific_gravity_rel_air=specific_gravity
            )
            
            V2 = f"{V2:,.3f} m3"

            st.success(f"Volume at state 2 = {V2}")

        except ValueError as e:
                st.error(str(e))

with st.expander("Useful Info"):
    st.subheader("Standard Conditions")
    st.write("Pressure: 101.325 kPa\n\n"
             "Temperature: 15°C")
    
    st.subheader("Normal Conditions")
    st.write("Pressure: 101.325 kPa\n\n"
             "Temperature: 20°C")
    

        
with st.container(border=True):
    st.subheader("Modified Ideal Gas Law", divider=divider_color)
    
    st.markdown("""
                The Ideal Gas Law can be modified with compressibility factor, $Z$, as follows:
                """)
    
    st.latex(r"""
             PV = ZnR_uT
             """)
    
    st.markdown("""
                This equation can be rearranged to compare the properties of a gas at two different states, assuming the number of moles remains constant, and the universal gas constant
                cancels on each side:
                """)
    
    st.latex(r"""
             \frac{P_1V1}{Z_1T_1} = \frac{P_2V2}{Z_2T_2}
             """)
    
    st.markdown("""
                Solving for $V_2$, a formula is derived to convert volume/volume flow rate at one specified state to another:
                """)
    
    st.latex(r"""
             V_2 = V_1\frac{Z_2T_2P_1}{Z_1T_1P_2}
             """)
    
    st.markdown("""
                where:
                
                - $V_1$ and $V_2$ are the volume or volume flow rate (any volume/volume flow units)
                - $Z_1$ and $Z_2$ are the compressibility factor of the gas at state 1 and 2 (dimensionless)
                - $T_1$ and $T_2$ are the temperature of the gas at state 1 and 2 [K]
                - $P_1$ and $P_2$ are the presure of the gas at state 1 and 2 (any pressure units, absolute)
                """)
    
    st.subheader("GPSA Z-Factor Correlation", divider=divider_color)
    
    st.markdown("""
                For convenience, the GPSA Z-Factor (compressibility factor) correlation can be used in lieu of manually entering the Z-factor at each state.
                The procedure, from Section 17 Eqns 17-12 and 17-13, is shown below:
                """)
    
    st.latex(r"""
             F_{pv} = \sqrt{1 + \frac{P_{avg} \cdot 0.0527 \cdot 10^5 \cdot 10^{1.785\gamma}}{T_{avg}^{3.825}}}
             """)
    st.latex(r"""
             Z_{avg} = \frac{1}{F_{pv}^2}
             
             
             """)
    st.markdown("""
                where:
                
                - $P_{avg}$ is the pressure [kPa, abs]
                - $T_{avg}$ is the temperature [K]
                - $/gamma$ is the specific gravity relative to air of the gas (dimensionless)
                - $Z_{avg}$ is the Z-factor/compressibility factor (dimensionless)
                """)