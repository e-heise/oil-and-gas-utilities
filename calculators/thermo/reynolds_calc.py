def reynolds_number (
    density_kg_m3: float,
    velocity_m_s: float,
    diameter_m: float,
    dynamic_viscosity_pa_s: float
) -> float:
    _validate_positive(density_kg_m3, "density_kg_m3")
    _validate_positive(velocity_m_s, "velocity_m_s")
    _validate_positive(diameter_m, "diameter_m")
    _validate_positive(dynamic_viscosity_pa_s, "dynamic_viscosity_pa_s")
    
    result = density_kg_m3 * velocity_m_s * diameter_m / dynamic_viscosity_pa_s
    
    return result
    
def _validate_positive(value: float, name:str) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")