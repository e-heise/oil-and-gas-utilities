import streamlit as st
from calculators.geometry.vessel_volume_calc import vessel_volume

divider_color = "red"

if "vessel_type" not in st.session_state:
    st.session_state.vessel_type = "Horizontal"

st.title("Vessel Volume")


with st.container(border=True):
    col1, col2, col3 = st.columns(3)    
    with col1:
        vessel_type = st.radio(
                "Vessel Type",
                ["Horizontal", "Vertical", "Spherical"],
                key="vessel_type"
                )
        
    with col2:
        head_type = st.radio(
                "Head Type",
                ["Flat", "Elliptical", "Hemispherical"],
                disabled=(st.session_state.vessel_type=="Spherical")
                )
    
    length = st.number_input("Length/Height [m]",
                                min_value=0.0,
                                value=2.0,
                                disabled=(st.session_state.vessel_type=="Spherical"))
    
    diameter = st.number_input("Inner Diameter [m]",
                                min_value=0.0,
                                value=1.2)
    
    liquid_height = st.number_input("Liquid Height [m]",
                                    min_value=0.0,
                                    value=0.6)

if st.button("Calculate", type="primary", width="stretch"):    
    try:
        volume = vessel_volume(
            vessel_type=vessel_type,
            head_type=head_type,
            length_m=length,
            diameter_m=diameter,
            liquid_height_m=liquid_height
        )
        
        volume = f"{volume:.3f} m3"
    
        st.success(f"Calculated volume: {volume}")
    
    except ValueError as e:
        st.error(str(e))

with st.container(border=True):
    st.subheader("Vessel Shell Partial Volume", divider=divider_color)

    st.markdown("""
                Partial volume equations for shells of different types are shown below.
                """)
    st.write("Vertical cylinder:")
    
    st.latex(r"""
             V_p = \frac{\pi}{4} D_i^2 h
             """)
    
    st.write("Horizontal cylinder:")

    st.latex(r"""
             V_p = L D_i^2 \left(0.25 \arccos\left(1-2\frac{h}{D_i}\right) - \left(0.5-\frac{h}{D_i}\right) \sqrt{\frac{h}{D_i} - \left(\frac{h}{D_i}\right)^2}\right)
             """)
    
    st.write("Spherical vessel:")

    st.latex(r"""
             V_p = \left( \frac{\pi h^2 D_i}{2} \right) - \left( \frac{\pi h^3}{3} \right)
             """)

    st.markdown("""
                where:
                
                - $V_p$ is the partial volume of the shell [m<sup>3</sup>]
                - $D_i$ is the inner diamter of the vessel [m]
                - $h$ is the height of the liquid in the vessel [m]
                
                The $arccos$ argument is provided in radians.
                """,
                unsafe_allow_html=True)

    st.subheader("Vessel Head Partial Volume", divider=divider_color)
    
    st.markdown("""
                Partial volume for vessel heads of different types are shown below.
                """)
    
    st.write("Elliptical head (horizontal vessel):")

    st.latex(r"""
             V_p = D_i^3 \frac{\pi}{24} \left( 3\left(\frac{h}{D_i}\right)^2 - 2\left(\frac{h}{D_i}\right)^3 \right)
             """)
    
    st.write("Elliptical head (vertical vessel):")

    st.latex(r"""
             V_p = D_i^3 \frac{\pi}{48} \left( 3\left(\frac{h}{z}\right)^2 - \left(\frac{h}{z}\right)^3 \right)
             """)
    
    st.write("Hemisperhical head (horizontal vessel):")

    st.latex(r"""
             V_p = D_i^3 \frac{\pi}{12} \left( 3\left(\frac{h}{D_i}\right)^2 - 2\left(\frac{h}{D_i}\right)^3 \right)
             """)
    
    st.write("Hemispherical head (vertical vessel):")

    st.latex(r"""
             V_p = \frac{\pi}{3} \left( 2R_c^3 - h^2 \left( 3R_c - h \right) \right)
             """)
    
    st.markdown("""
                where:
                
                - $V_p$ is the partal volume of the head [m<sup>3</sup>]
                - $D_i$ is the inner diameter of the vessel [m]
                - $h$ is the height of the liquid in the vessel/head [m]
                - $z$ is the dish depth [m]
                - $R_c$ is the head radius [m]
                """)