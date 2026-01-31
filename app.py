# start the server with streamlit run app.py

import streamlit as st

from calculators.thermo.reynolds_calc import reynolds_number

if __name__ == "__main__":
    # main()
    home_page = st.Page("pages/main/home.py", title="Home")
    
    about_page = st.Page("pages/main/about.py", title="About")
    
    # conversion
    gas_conditions_page = st.Page("pages/conversion/gas_conditions_page.py", title="Gas Flow Converter")
    air_gas_flow_converter_page = st.Page("pages/conversion/air_gas_flow_converter_page.py", title="Air-to-Gas Flow Rate Converter")
    
    # electrical
    
    # geometry
    vessel_volume_page = st.Page("pages/geometry/vessel_volume_page.py", title="(x) Vessel Volume")
    
    # heat-transfer
    
    # math
    
    # pipe_flow
    piping_pressure_drop_page = st.Page("pages/pipe_flow/piping_pressure_drop_page.py", title="(x) Piping Pressure Drop")
    erosional_velocity_page = st.Page("pages/pipe_flow/erosional_velocity_page.py", title="Erosional Velocity")
    
    # pressure_changers
    npsh_page = st.Page("pages/pressure_changers/npsh_page.py", title="Pump NPSH")
    pump_compressor_power_page = st.Page("pages/pressure_changers/pump_compressor_power_page.py", title="(x) Pump/Compressor Power")
    control_valve_sizing_page = st.Page("pages/pressure_changers/control_valve_page.py", title="(x) Control Valve Sizing")
    
    # thermo
    reynolds_page = st.Page("pages/thermo/reynolds_page.py", title="Reynolds Number")
    
    # unit_ops
    dehy_circ_rate_page = st.Page("pages/unit_ops/glycol_circ_rate_page.py", title="(x) Glycol Dehy Circulation Rate")
    amine_circ_rate_page = st.Page("pages/unit_ops/amine_circ_rate_page.py", title="(x) Amine Circulation Rate")
    
    # information
    control_valve_catalog_page = st.Page("pages/info/control_valve_catalog_page.py", title="(x) Control Valve Catalog")
    
    # utilities
    barometric_pressure_page = st.Page("pages/utilities/barometric_pressure_page.py", title="Barometric Pressure")
    
    pages = {
        "Main": [
            home_page,
            about_page
        ],
        
        "Conversion": [
            gas_conditions_page,
            air_gas_flow_converter_page,
        ],
        
        "Electrical": [
            
        ],
        
        "Geometry": [
            vessel_volume_page
        ],
        
        "Heat Transfer": [
            
        ],
        
        "Math": [
            
        ],
        
        "Pipe Flow": [
            piping_pressure_drop_page,
            erosional_velocity_page
        ],
        
        "Pressure Changers": [
          npsh_page,
          pump_compressor_power_page,
          control_valve_sizing_page,
        ],
        
        "Thermodynamics": [
            reynolds_page,
        ],
        
        "Unit Operations": [
            dehy_circ_rate_page,
            amine_circ_rate_page
        ],
        
        "Information": [
            control_valve_catalog_page
        ],
        
        "Utilities": [
            barometric_pressure_page
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()