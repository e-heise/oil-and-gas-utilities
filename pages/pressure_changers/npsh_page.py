import streamlit as st
from calculators.pressure_changers.npsh_calc import npsh_simple, npsh_advanced
import math

divider_color = "red"

if "roughness_type" not in st.session_state:
    st.session_state.roughness_type = "Carbon Steel (45.72 µm)"
    
if "opt_advanced_calc" not in st.session_state:
    st.session_state.opt_advanced_calc = False
    
if "methodology_expanded" not in st.session_state:
    st.session_state.methodology_expanded = False
    
def update_methodology_expander_state():
    st.session_state.methodology_expanded = st.session_state.methodology_expander_key

st.title("Centrifugal Pump NPSHa")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Basic", divider=divider_color)
        atmospheric_pressure = st.number_input("Atmospheric Pressure [kPa]",
                                               min_value=0.0,
                                               value=101.325,
                                               help="Atmospheric pressure has a significant impact on NPSHa.\n\n"
                                               "Ensure the correct atmospheric pressure is used.")
        
        inlet_pressure = st.number_input("Inlet Pressure (Px) [kPag]",
                                        min_value=0.0,
                                        value=1.7237,
                                        help="Pressure measured at the free surface of the liquid in the tank/vessel.")
        
        vapor_pressure = st.number_input("Fluid Vapor Pressure (Pv) [kPa abs]",
                                        min_value=0.0,
                                        value=1.71)
        
        fluid_density = st.number_input("Fluid Density ρ [kg/m3]",
                                        min_value=0.0,
                                        value=999.0)

        relative_height = st.number_input("Relative Height (hx) [m]",
                                        value=1.5,
                                        help="Relative height between the centerline of the pump suction and the top of the free liquid surface in the tank/vessel.")
        
        flow_rate = st.number_input("Fluid Flow Rate [m3/hr]",
                                    min_value=0.0,
                                    value=1.5)

        head_loss = st.number_input("Head Loss (hfx) [m]",
                                    min_value=0.0,
                                    value=0.5,
                                    disabled=(st.session_state.opt_advanced_calc),
                                    help="Equivalent head loss due to friction of fluid flow in suction piping.")
        
        pipe_diameter = st.number_input("Pipe Inner Diameter [mm]",
                                min_value=0.0,
                                value=50.0)
    
with col2:
    with st.container(border=True, height="stretch"):
        st.subheader("Advanced", divider=divider_color)
        opt_advanced_calc  = st.checkbox("Use head loss calculation?",
                                         key="opt_advanced_calc")
        viscosity = st.number_input("Dynamic Viscosity [cP]",
                                    min_value=0.0,
                                    value=1.138,
                                    disabled=not st.session_state.opt_advanced_calc)
        
        pipe_material = st.selectbox("Pipe Material",
                                ("Carbon Steel (45.72 µm)", "Stainless Steel (1.524 µm)", "Custom"),
                                key="roughness_type",
                                    disabled=not st.session_state.opt_advanced_calc)
        
        roughness_input = st.number_input("Pipe Roughness [µm]",
                                        min_value=0.0,
                                        value=45.72,
                                        disabled=(not st.session_state.roughness_type=="Custom" or
                                                  not st.session_state.opt_advanced_calc))
        
        pipe_length = st.number_input("Pipe Equivalent Length [m]",
                                min_value=0.0,
                                value=10.0,
                                    disabled=not st.session_state.opt_advanced_calc)     

if st.button("Calculate", type="primary", width="stretch"):
    try:
        area = math.pi / 4 * (pipe_diameter/1000)**2
        velocity = (flow_rate / 3600) / area
        
        if st.session_state.roughness_type == "Custom":
            roughness = roughness_input
        else:
            match st.session_state.roughness_type:
                case "Carbon Steel (45.72 µm)":
                    roughness = 45.72
                case "Stainless Steel (1.524 µm)":
                    roughness = 1.524
        
        if st.session_state.opt_advanced_calc == True:
            NPSHa = npsh_advanced(
                pressure1_kPa=inlet_pressure+atmospheric_pressure,
                vapor_pressure_kPa=vapor_pressure,
                fluid_density_kg_m3=fluid_density,
                relative_height_m=relative_height,
                velocity_m_s=velocity,
                pipe_diameter_m=pipe_diameter/1000,
                viscosity_Pa_s=viscosity/1000,
                pipe_roughness_m=roughness/10**6,
                equivalent_length_m=pipe_length
                )
            NPSHa = f"{NPSHa:.2f} m"

            st.success(f"Calculated NPSHa: {NPSHa}")
            
        elif st.session_state.opt_advanced_calc == False:
            NPSHa = npsh_simple(
                pressure1_kPa=inlet_pressure+atmospheric_pressure,
                vapor_pressure_kPa=vapor_pressure,
                fluid_density_kg_m3=fluid_density,
                relative_height_m=relative_height,
                velocity_m_s=velocity,
                head_loss_m=head_loss
                )
            
            NPSHa = f"{NPSHa:.2f} m"

            st.success(f"Calculated NPSHa: {NPSHa}")

    except ValueError as e:
        st.error(str(e))
        
with st.container(border=True):
    st.subheader("Net Positive Suction Head", divider=divider_color)
    st.markdown("""
                The Net Positive Suction Head Available (NPSHa) quantifies how close a fluid is to cavitating in a pump.
                NPSHa must be higher than the Net Positive Suction Head Required (NPSHr) of a given pump.
                
                Fluids with high vapor pressure (i.e. condensate, LPG/NGL, etc.) lead to a lower NPSHa.
                High friction losses and insufficient elevation difference between suction tank level and suction nozzle centerline
                also reduce NPSHa.
                
                NPSHa is calculated as follows:                
                """)
    
    st.latex(r"""
             NPSHa = \frac{1000 \cdot (P_x - P_{vp})}{\rho g} + z_x + \frac{V_x^2}{2 g} - h_{fx}
             """)
    
    st.markdown("""
                where:
                
                - $NPSHa$ is the Net Positive Suction Head [m]
                - $P_x$ is the pressure at the free surface of the fluid in the upstream tank/vessel [kPa abs]
                - $P_v$ is the vapor pressure of the fluid [kPa abs]
                - $\\rho$ is the density of the fluid [kg/m³]
                - $g$ is the acceleration due to gravity = 9.80665 m/s
                - $z_x$ is the relative height between the pump suction centerline and the surface of the free liquid in the upstream tank/vessel [m]
                - $V_x$ is the average velocity of the fluid in the suction piping, measured at the free liquid surface
                - $h_{fx}$ is the head losses due to friction in the suction piping [m]
                """)

    st.subheader("Friction Factor and Head Losses", divider=divider_color)
    st.markdown("""
                For the purposes of the NPSHa calculation above, the manual head losses entry can be subsituted for an automatic
                calculation using the Darcy-Weisbach equation. The head losses are calculated as follows:
                """)
    st.latex(r"""
             h_L = \frac{f_m L V^2}{2 g D}
             """)
    st.markdown("""
                where:
                
                - $h_L$ is the calculated head losses [m]
                - $f_m$ is the Darcy Friction Factor (dimensionless)
                - $L$ is the equivalent length of piping through which head losses are to be calculated [m]
                - $V$ is the average velocity of the fluid in the suction piping
                - $g$ is the acceleration due to gravity (9.80665 m/s)
                - $D$ is the inner diameter of the pipe [m]
                """)
    st.markdown("""
                The Darcy Friction Factor, $f$, is an empirical coefficient used to quantify head losses for pipe or channel flow.
                Equations for the Darcy Friction factor are typically implicit in nature, so for simplicity, an approximation is used
                here to avoid iterative calculation. \n\n
                
                Serghides' Solution provides high accuracy for full pipe flow, and is based on the Colebrook-White equation.
                Calculation proceeds as follows:
                """)
    st.latex(r"""
            A = -2 \log\left(\frac{\epsilon/D}{3.7} + \frac{12}{Re}\right)
            """)
    st.latex(r"""
            B = -2 \log\left(\frac{\epsilon/D}{3.7} + \frac{2.51A}{Re}\right)
            """)
    st.latex(r"""
            C = -2 \log\left(\frac{\epsilon/D}{3.7} + \frac{2.51B}{Re}\right)
            """)
    st.latex(r"""
            \frac{1}{\sqrt{f}} = A - \frac{(B-A)^2}{C-2B+A}
            """)
    st.latex(r"""
             f = \left(\frac{1}{\sqrt{f}}\right)^{-2}
             """)
    st.markdown("""
                where:
                
                - $\\epsilon$ is the roughness of the pipe wall material [m]
                - $D$ is the inner diameter of the pipe [m]
                - $Re$ is the Reynolds number of the flow in the pipe
                """)