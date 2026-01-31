from utilities.constants import constants
import math

import streamlit as st

def npsh_simple(
    pressure1_kPa: float,
    vapor_pressure_kPa: float,
    fluid_density_kg_m3: float,
    relative_height_m: float,
    velocity_m_s: float,
    head_loss_m: float, 
    
) -> float:
    #TODO: add validation
    
    Px = pressure1_kPa
    Pvp = vapor_pressure_kPa
    rho = fluid_density_kg_m3
    g = constants['g']
    zx = relative_height_m
    Vx = velocity_m_s
    hfx = head_loss_m
    
    # calculate NPSHa via GPSA Eqn. 12-6b
    NPSH = (1000 * (Px - Pvp) / rho / g) + zx + (Vx**2 / 2 / g) - hfx
    
    return NPSH
    

def npsh_advanced(
    pressure1_kPa: float,
    vapor_pressure_kPa: float,
    fluid_density_kg_m3: float,
    relative_height_m: float,
    velocity_m_s: float,
    pipe_diameter_m: float, 
    viscosity_Pa_s: float,
    pipe_roughness_m: float,
    equivalent_length_m: float,  
    
) -> float:
    #TODO: add validation
    
    Px = pressure1_kPa
    Pvp = vapor_pressure_kPa
    rho = fluid_density_kg_m3
    g = constants['g']
    zx = relative_height_m
    Vx = velocity_m_s
    d = pipe_diameter_m
    mu = viscosity_Pa_s
    epsilon = pipe_roughness_m
    L = equivalent_length_m
    
    # calculate Reynolds Number
    Re = rho * Vx * d / mu
    
    # calculate friction factor via Serghides' solution
    A = -2 * math.log(epsilon/d/3.7 + 12/Re)
    B = -2 * math.log(epsilon/d/3.7 + 2.51*A/Re)
    C = -2 * math.log(epsilon/d/3.7 + 2.51*B/Re)
    f_inv = A - ((B-A)**2 / (C - 2*B + A))
    f = f_inv**-2
    
    # calculate head loss via GPSA eqn. 17-6
    hL = f * L * Vx**2 / 2 / g / d
    hfx = hL
    
    # calculate NPSHa via GPSA Eqn. 12-6b
    NPSH = (1000 * (Px - Pvp) / rho / g) + zx + (Vx**2 / 2 / g) - hfx
    
    return NPSH
    
    