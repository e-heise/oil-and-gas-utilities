from utilities.thermo_utils import z_factor_GPSA

def gas_conditions_converter (
    pressure1_Pa: float,
    temperature1_K: float,
    compressibility1: float,
    volume1_m3: float,
    pressure2_Pa: float,
    temperature2_K: float,
    compressibility2: float,
    calc_z_factor: bool,
    specific_gravity_rel_air = None  
) -> float:
    _validate_positive(pressure1_Pa, "pressure1")
    _validate_positive(temperature1_K, "temperature1")
    _validate_positive(compressibility1, "compressibility1")
    _validate_positive(volume1_m3, "volume1")
    _validate_positive(pressure2_Pa, "pressure2")
    _validate_positive(temperature2_K, "temperature2")
    _validate_positive(compressibility2, "compressibility2")

    P1 = pressure1_Pa
    T1 = temperature1_K
    V1 = volume1_m3
    P2 = pressure2_Pa
    T2 = temperature2_K
    y = specific_gravity_rel_air
    
    if calc_z_factor:
        if y:
            Z1 = z_factor_GPSA(P1/1000, T1, y)
            Z2 = z_factor_GPSA(P2/1000, T2, y)
        else:
            raise TypeError("The option to calculate the Z factor was selected, but a valid specific gravity was not provided.")
    
    else:
        Z1 = compressibility1
        Z2 = compressibility2
        
    V2 = V1 * (Z2/Z1) * (T2/T1) * (P1/P2)
    
    return V2
    
def _validate_positive(value: float, name: str) -> None:
       if value <= 0.0:
        raise ValueError(f"{name} must be > 0")    