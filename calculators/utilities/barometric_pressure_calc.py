import math

def barometric_pressure(
    altitude_m: float
) -> float:
    #TODO: add validation
    
    H = altitude_m
    
    Pb = 101.325
    g0 = 9.80665
    M0 = 28.9644
    Hb = 0.0
    R_star = 8314.32
    Tmb = 288.15
    
    P = Pb * math.exp((-g0 * M0 * (H-Hb))/(R_star * Tmb))
    
    return P