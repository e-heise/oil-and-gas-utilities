import math

def air_gas_flow_converter(
    flowrate: float,
    specific_gravity: float,
) -> float:
    #TODO: add validation
    
    Q1 = flowrate
    SG = specific_gravity
    
    Q2 = Q1 / math.sqrt(SG)

    return Q2