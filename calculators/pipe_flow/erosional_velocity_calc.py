def erosional_velocity(
    service_factor: float,
    mixture_density_lb_ft3: float
    
) -> float:
    #TODO: add validation
    
    C = service_factor
    rho_m = mixture_density_lb_ft3
    
    # calculate erosional velocity
    Ve = C / rho_m**0.5
    
    return Ve

