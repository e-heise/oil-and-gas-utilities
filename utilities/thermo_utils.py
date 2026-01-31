def z_factor_GPSA(
    pressure_kPa: float,
    temperature_K: float,
    specific_gravity: float
) -> float:
    P = pressure_kPa
    T = temperature_K
    y = specific_gravity
    
    Fpv = ( 1 + (P * 0.0527 * 10**5 * 10**(1.785 * y)) / (T**3.825))**0.5
    Z  = 1 / Fpv**2
    
    return Z