import streamlit as st
import pandas as pd

from calculators.pipe_flow.erosional_velocity_calc import erosional_velocity

divider_color = "red"

st.title("Erosional Velocity")

with st.container(border=True):
    service_factor = st.number_input("Service Factor",
                                     min_value=0.0,
                                     value=100.0)

    mixture_density = st.number_input("Mixture Density [kg/m3]",
                                      min_value=0.0,
                                      value=900.0)
    
    if st.button("Calculate", type="primary", width="stretch"):
        try:
            Ve = erosional_velocity(
                service_factor=service_factor,
                mixture_density_lb_ft3=mixture_density/16.0185
            )
            
            Ve /= 3.28084
            
            Ve = f"{Ve:.2f} m/s"
            
            st.success(f"Erosional Velocity: {Ve}")
    
        except ValueError as e:
            st.error(str(e))
    
with st.container(border=True):
    st.subheader("API RP 14E Erosional Velocity", divider=divider_color)
    
    st.markdown("""
                The Erosional Velocity calculation from API RP 14E is widely used, but serves only as a guideline for upper
                velocity limits in piping. Varying degrees of sand/solid size and quantity will significantly change
                the effect service factor that is required. This equation is often applied to single-phase liquid flow and two-phase 
                gas/liquid flow. Erosion is generally not a concern for single-phase gas flow, where pressure drop and velocity 
                tend to dominate sizing.\n\n                 
            
                    
                Erosional velocity is calculated as follows:
                """)
    
    st.latex(r"""
             V_e = \frac{C}{\sqrt{\rho_m}}
             """)
    
    st.markdown("""
                where:
                
                - $V_e$ is the erosional velocity [ft/s]
                - $C$ is the service factor
                - $\rho_m$ is the mixture density [lb/ft3]
                
                The service factor, $C$, depends greatly on the particular service and sand/solids content in the fluid stream. 
                Below is a table showing recommended service factors for various fluid services:
                """)
    
    service_factors_data = {
        "Service": ["Solids-free, Non-Corrosive", "Solids-Free, Corrosive"],
        "Continous": ["150-200", "100"],
        "Intermittent": ["250", "125"]
    }
    df_service_factors = pd.DataFrame(service_factors_data)
    st.dataframe(df_service_factors, hide_index=True, width="content")
    
    st.markdown("""
                Note that the above service factors are to be used ***as a guideline only***. Actual design should use a more conservative service 
                factor, or ensure that actual velocities are sufficiently lower than the calculated erosional velocity to provide some margin.
                """)