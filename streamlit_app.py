import streamlit as st
from pathlib import Path
import sys

import pandas as pd
from io import BytesIO

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
st.caption("Version 0.1.0 - CH/CHO Thermodynamic Property Estimator")

st.write(
    """
    An open-source framework for thermodynamic property estimation, 
    reaction-space exploration, and early-stage process analysis.
    """
)
st.info(
    "Current release: thermodynamic property estimation "
    "for CH and CHO organic compounds."
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
        if not formula.strip():
            st.warning("Enter a molecular formula to calculate properties.")
        else: 
            try: 
                results = estimate_properties(formula)

                st.markdown("#### Formation Properties")

                h_col, g_col = st.columns(2)

                with h_col: 
                    st.metric(
                        r"$\Delta H_F^0$", 
                        f"{results["Estimated dHf (kJ/mol)"]:.1f} kJ/mol"
                    )
                with g_col: 
                    st.metric(
                        r"$\Delta G_F^0$", 
                        f"{results["Estimated dGf (kJ/mol)"]:.1f} kJ/mol"
                    )
                st.markdown("#### Combustion Properties")

                hc_col, gc_col = st.columns(2)

                with hc_col: 
                    st.metric(
                        r"$\Delta H_C^0$", 
                        f"{results["Estimated dHc (kJ/mol)"]:.1f} kJ/mol"
                    )
                with gc_col: 
                    st.metric(
                        r"$\Delta G_C^0$", 
                        f"{results["Estimated dGc (kJ/mol)"]:.1f} kJ/mol"
                    )
            except Exception as e: 
                st.error(
                    "Unable to calculate properties for this formula. "
                    "ANCETRA currently supports CH and CHO organic compounds."
                )

st.divider()
st.header("Batch Property Estimation")
st.write(
    """
    Upload a CSV or Excel file containing a **Formula** columns. 
    ANCETRA will estimate thermodynamic properties for each compound.
    """
)
uploaded_file = st.file_uploader(
    "Upload compound file", 
    type=["csv", "xlsx"]
)
if uploaded_file is not None: 
    try: 
        if uploaded_file.name.endswith(".csv"): 
            batch_df = pd.read_csv(uploaded_file)
        else: 
            batch_df = pd.read_excel(uploaded_file)
        if "Formula" not in batch_df.columns: 
            st.error(
                "The uploaded file must contain a column named 'Formula'."
            )
        else: 
            st.markdown("#### Input Preview")
            st.dataframe(batch_df.head(), use_container_width=True)
            if st.button(
                "Calculate Batch Properties", 
                type="primary"
            ): 
                batch_results = []

                for _, row in batch_df.iterrows(): 
                    formula_batch = str(row["Formula"]).strip()
                    try: 
                        properties = estimate_properties(formula_batch)
                        result_row = row.to_dict()
                        result_row.update({
                            "Estimated dHf (kJ/mol)": 
                                properties["Estimated dHf (kJ/mol)"], 
                            "Estimated dGf (kJ/mol)": 
                                properties["Estimated dGf (kJ/mol)"], 
                            "Estimated dHc (kJ/mol)": 
                                properties["Estimated dHc (kJ/mol)"], 
                            "Estimated dGc (kJ/mol)": 
                                properties["Estimated dGc (kJ/mol)"],
                            "Status": "Calculated"
                        })
                    except Exception: 
                        result_row = row.to_dict()
                        result_row.update({
                            "Estimated dHf (kJ/mol)": None, 
                            "Estimated dGf (kJ/mol)": None, 
                            "Estimated dHc (kJ/mol)": None, 
                            "Estimated dGc (kJ/mol)": None,
                            "Status": "Unable to calculate"
                        })
                    batch_results.append(result_row)
                results_df = pd.DataFrame(batch_results)
                st.markdown("#### Batch Results")
                st.dataframe(
                    results_df, use_container_width=True
                )

                csv = results_df.to_csv(
                    index=False
                ).encode("utf-8")

                excel_buffer = BytesIO()
                with pd.ExcelWriter(
                    excel_buffer, engine="openpyxl"
                ) as writer: 
                    results_df.to_excel(
                        writer, index=False,  sheet_name="ANCETRA Results"
                    )
                download_col1, download_col2 = st.columns(2)
                with download_col1: 
                    st.download_button(
                        label="Download Excel Results", 
                        data=excel_buffer.getvalue(),
                        file_name="ANCETRA_results.xlsx", 
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        )
                    )
                with download_col2: 
                    st.download_button(
                        label="Download CSV Results", 
                        data=csv, 
                        file_name="ANCETRA_results.csv", 
                        mime="text/csv"
                    )
    except Exception as e: 
        st.error(
            "Unable to read or process the uploaded file. "
            "Please upload a valid CSV or Excel file."
        )

with st.expander("About the CH/CHO Model"): 
    st.markdown(
        """
        This version of ANCETRA estimates standard thermodynamic properties
        for organic compounds containing carbon, hydrogen, and oxygen using
        the CH/CHO oxygen-demand model published by Anastasi et al. (2026).

        **Current Scope**
        - CH and CHO organic compounds
        - Standard enthalpy of formation
        - Standard Gibbs free energy of formation
        - Standard enthalpy of combustion
        - Standard Gibbs free energy of combustion
        - Single-compound and batch estimation

        Additional elemental compositions and thermodynamics properties are under development.
        """
    )

st.divider()
st.caption(
    "ANCETRA is open-source research software developed for "
    "thermodynamic property estimation and reaction analysis."
)
st.markdown(
    "[GitHub Repository] https://github.com/tonyanastasi22/biomass-thermo-model "
    "[Model Publication] https://psecommunity.org/LAPSE:2026.0370 "
)