import streamlit as st
from pathlib import Path
import sys

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path: 
    sys.path.insert(0, str(SRC_DIR))

from cho_thermo.thermo import estimate_properties

st.set_page_config(
    page_title="ANCETRA", 
    layout="wide"
)

st.title("ANCETRA")

st.subheader("Anastasi Chemical Energetics, Thermodynamics & Reaction Analysis")

st.write(
    """
    An open-source framework for thermodynamic property estimation, 
    reaction-space exploration, and early-stage process analysis.
    """
)

st.divider()

st.header("Thermodynamic Property Estimator")

col1, col2 = st.columns([1,2])

with col1: 
    st.subheader("Compound Input")
    formula = st.text_input(
        "Molecular Formula", 
        placeholder="e.g., C6H12O6"
    )
    calculate = st.button(
        "Calculate Properties", 
        type="primary"
    )

with col2: 
    st.subheader("Predicted Properties")
    if calculate: 
        results = estimate_properties(formula)
        
        st.metric(
            r"$\Delta H_F^0$", 
            f"{results["Estimated dHf (kJ/mol)"]:.1f} kJ/mol"
        )
        
        st.metric(
            r"$\Delta G_F^0$", 
            f"{results["Estimated dGf (kJ/mol)"]:.1f} kJ/mol"
        )