import math

def vessel_volume(
    vessel_type: str,
    head_type: str,
    length_m: float,
    diameter_m: float,
    liquid_height_m: float
) -> float:
    _validate_positive_(length_m, "length_m")
    _validate_positive_(diameter_m, "diameter_m")
    _validate_positive_(liquid_height_m, "liquid_height_m")
    _validate_liquid_height_(vessel_type, head_type, diameter_m, length_m, liquid_height_m)
    
    vessel_type = vessel_type
    head_type = head_type
    L = length_m
    Di = diameter_m
    h = liquid_height_m
    
    match vessel_type:
        case "Horizontal":
            Vps = shell_volume(
                vessel_type=vessel_type,
                diameter_m=Di,
                length_m=L,
                liquid_height_m=h
            )

            Vph_left = head_volume(
                vessel_type=vessel_type,
                head_type=head_type,
                diameter_m=Di,
                liquid_height_m=h
            )
            
            Vph_right = head_volume(
                vessel_type=vessel_type,
                head_type=head_type,
                diameter_m=Di,
                liquid_height_m=h
            )
            
            Vp_total = Vps + Vph_left + Vph_right
        
        case "Vertical":
            if head_type == "Elliptical":
                z = Di / 4
            else:
                z = Di / 2

            hb = min(h, z)
            ht = z - max(0, h - (L + z))

            if head_type != "Flat":
                h = min(max(0, h - z), L)
            
            Vps = shell_volume(
                vessel_type=vessel_type,
                diameter_m=Di,
                length_m=L,
                liquid_height_m=h
            )
            
            Vph_bottom = head_volume(
                vessel_type=vessel_type,
                head_type=head_type,
                diameter_m=Di,
                liquid_height_m=hb
            )
            
            Vph_top = head_volume(
                vessel_type=vessel_type,
                head_type=head_type,
                diameter_m=Di,
                liquid_height_m=z
            ) - head_volume(
                vessel_type=vessel_type,
                head_type=head_type,
                diameter_m=Di,
                liquid_height_m=ht
            )
            
            Vp_total = Vps + Vph_bottom + Vph_top
        
        case "Spherical":
            Vp_total = shell_volume(
                vessel_type=vessel_type,
                diameter_m=Di,
                length_m=L,
                liquid_height_m=h
            )
            
    return Vp_total
    
    
def shell_volume(
    vessel_type: str,
    diameter_m: float,
    length_m: float,
    liquid_height_m: float
) -> float:
    vessel_type = vessel_type
    Di = diameter_m
    L = length_m
    h = liquid_height_m
    
    match vessel_type:
        case "Horizontal":
            Vp = L * Di**2 * (0.25) * math.acos(1 - 2*h/Di) - (0.5 - h/Di) * math.sqrt(h/Di - (h/Di)**2)
        
        case "Vertical":
            Vp = math.pi / 4 * Di**2 * h
        
        case "Spherical":
            Vp = (math.pi * h**2 * Di/2) - (math.pi * h**3 / 3)

    return Vp

def head_volume(
    vessel_type: str,
    head_type: str,
    diameter_m: float,
    liquid_height_m: float,
) -> float:
    vessel_type = vessel_type
    head_type = head_type
    Di = diameter_m
    h = liquid_height_m
    
    match head_type:
        case "Flat":
            Vp = 0.0
        
        case "Elliptical":
            if vessel_type == "Horizontal":
                C = 0.5
                Vp = Di**3 * C * math.pi / 12 * (3*(h/Di)**2 - 2*(h/Di)**3)
            elif vessel_type == "Vertical":
                z = Di/4
                C = 0.5
                Vp = Di**3 * C * math.pi / 24 * (3*(h/z)**2 - (h/z)**3)
        
        case "Hemispherical":
            if vessel_type == "Horizontal":
                Vp = Di**3 * math.pi / 12 * (3 * (h/Di)**2 - 2*(h/Di)**3)
            elif vessel_type == "Vertical":
                Rc = Di/2
                Vp  = math.pi / 3 * h**2 * (3*Rc - h)
                
    return Vp

def _validate_positive_(value: float, name:str) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")

def _validate_liquid_height_(
    vessel_type: str,
    head_type: str, 
    diameter_m: float, 
    length_m: float, 
    liquid_height_m: float
    ) -> None:
        Di = diameter_m
        L = length_m
        h = liquid_height_m
        
        if vessel_type == "Horizontal":
            h_max = Di
        
        elif vessel_type == "Vertical":
            if head_type == "Flat":
                h_max = L
            elif head_type =="Elliptical":
                h_max = L + 2*(Di/4)
            elif head_type == "Hemispherical":
                h_max = L + 2*(Di/2)
        
        elif vessel_type == "Spherical":
            h_max = Di
            
        if h > h_max:
            raise ValueError(f"Liquid height must be below {h_max:.3f} m")