"""
Contains thermodynamic property estimation model
"""

from .constants import *

from .formula import *
from .version import MODEL_VERSION

def oxygen_demand(c: float, h: float, o: float) -> float: 
    """
    Stoichiometric oxygen demand for complete combustion. 
    """
    return c + h/4 - o/2

def estimate_combustion_enthalpy(nu_o2: float) -> float: 
    """
    Return positive enthalpy of combustion in kJ/mol. 
    """
    return THORNTON_INT + THORNTON_SLOPE * nu_o2

def estimate_combustion_gibbs(delta_h_c: float) -> float: 
    """
    Return positive Gibbs free energy of combustion in kJ/mol.
    """
    return DG_FROM_DH_SLOPE * delta_h_c + DG_FROM_DH_INT

def estimate_properties(formula: str) -> dict: 
    """
    Estimate CHO thermodynamic properties from a molecular formula.
    """
    counts = parse_formula(formula)

    unsupported = set(counts) - {'C', 'H', 'O'}
    if unsupported: 
        raise ValueError(
            "This estimator supports CHO compounds only. "
            f"Unsupported elements: {sorted(unsupported)}"
        )
    c = float(counts.get("C", 0.0))
    h = float(counts.get("H", 0.0))
    o = float(counts.get("O", 0.0))

    if c <= 0: 
        raise ValueError("The CHO model requires a carbon-containing compound.")
    
    nu_o2 = oxygen_demand(c, h, o)

    if nu_o2 <= 0: 
        raise ValueError(
            "Calculated oxygen demand is non-positive; "
            "the formula may be outside the model scope."
        )
    
    delta_h_c = estimate_combustion_enthalpy(nu_o2)
    delta_g_c = estimate_combustion_gibbs(delta_h_c)

    delta_h_f = delta_h_c + (c * HF_CO2) + ((h/2) * HF_H2O_L)
    delta_g_f = delta_g_c + (c * GF_CO2) + ((h/2) * GF_H2O_L)

    return {
        "Formula": formula, 
        "C": c, "H": h, "O": o, 
        "Oxygen Demand (mol O2/mol)": nu_o2, 
        "Estimated dHc (kJ/mol)": delta_h_c, 
        "Estimated dGc (kJ/mol)": delta_g_c, 
        "Estimated dHf (kJ/mol)": delta_h_f, 
        "Estimated dGf (kJ/mol)": delta_g_f, 
        "Model Version": MODEL_VERSION,
    }