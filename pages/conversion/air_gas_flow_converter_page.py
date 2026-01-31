import streamlit as st
from calculators.conversion.air_gas_flow_converter_calc import air_gas_flow_converter


if "density_choice" not in st.session_state:
    st.session_state.density_choice = False
    
st.title("Air-to-Gas Flow Rate Converter")

with st.container(border=True):
    flow_rate = st.number_input("Gas Flow Rate",
                                min_value=0.0,
                                value=100.0)

    density_choice = st.radio("Gas weight method",
                              ["Molecular Weight", "Specific Gravity relative to Air"],
                              key="density_choice")
    
    molecular_weight = st.number_input("Molecular Weight of Gas [kg/kmol]",
                                       min_value=0.0,
                                       value=17.382,
                                       disabled=(not st.session_state.density_choice == "Molecular Weight"))
    
    specific_gravity = st.number_input("Specific Gravity relative to Air",
                                       min_value=0.0,
                                       value=0.60,
                                       disabled=(not st.session_state.density_choice == "Specific Gravity relative to Air"))
    
    if st.button("Calculate", type="primary", width="stretch"):
        try:
            if st.session_state.density_choice == "Molecular Weight":
                SG = molecular_weight / 28.97
            elif st.session_state.density_choice == "Specific Gravity relative to Air":
                SG = specific_gravity
            
            Q2 = air_gas_flow_converter(
                                        flowrate=flow_rate,
                                        specific_gravity=SG)
            
            Q2 = f"{Q2:.3f}"

            st.success(f"Gas Flow Rate: {Q2}")

        except ValueError as e:
            st.error(str(e))
            
with st.container(border=True):
    st.subheader("Air-to-Gas Conversion")

    st.markdown("""
                A given flow rate of air can be converted to and equivalent rate in gas flow. This conversion is often required when dealing with 
                low pressure systems - fuel gas regulators, tank venting requirements, etc.\n
                The equation is shown below:
                """)
    
    st.latex(r"""
             Q_{gas} = Q_{air} \cdot \frac{1}{\sqrt{SG}}
             """)
    
    st.markdown("""
                where:
                
                - $Q_{gas}$ is the flow rate of gas (any units of *actual* volume flow rate)
                - $Q_{air}$ is the flow rate of air (any units of *actual* volume flow rate)
                - $SG$ is the specific gravity of the gas, relative to air (dimensionless)
                
                This correlation is an idealization, and ***is only applicable when the following assumptions hold true***:
                - the gas behaves as an ideal gas, limiting this correlation to relatively low pressures
                - conditions (temperature, pressure) are identical between air and the gas in question
                - conversion works for *actual* volume flow rates only, not standard (molar) flow rates
                
                """)

