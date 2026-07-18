from pathlib import Path
import pandas as pd
from .thermo import estimate_properties

def estimate_dataframe(
        input_df: pd.DataFrame, 
        compound_column: str = "Compound", 
        formula_column: str = "Formula", 
) -> pd.DataFrame: 
    """
    Estiamte thermodynamic properties for every row in a DataFrame. 

    Parameters: 
        - input_df: 
            Input table containing compound names and molecular formulas. 
        - compound_column: 
            Name of the compound-name column. 
        - formula_column: 
            Name of the molecular-formula column.
    Returns: 
        - pd.DataFrame: 
            Original input columns plus estimated thermodynamic properties.
    """

    if formula_column not in input_df.columns: 
        raise ValueError(
            f"Required column '{formula_column}' was not found."
        )
    rows: list[dict] = []

    for _, row in input_df.iterrows(): 
        compound = row.get(compound_column, "")
        formula_value = row.get(formula_column, "")

        if pd.isna(formula_value): 
            formula = ""
        else: 
            formula = str(formula_value).strip()
        base_result = row.to_dict()
        if not formula: 
            base_result["Status"] = "Missing formula"
            rows.append(base_result)
            continue
        try: 
            estimates = estimate_properties(formula)
            base_result.update(estimates)
            base_result["Status"] = "OK"
        except Exception as exc: 
            base_result["Status"] = f"Error: {exc}"
        rows.append(base_result)
    return pd.DataFrame(rows)

def process_excel_workbook(
        input_file: str | Path, 
        output_file: str | Path, 
        sheet_name: str | int = 0, 
) -> Path: 
    """
    Read an Excel workbook, estimate properties, and save the results. 
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists(): 
        raise FileNotFoundError(
            f"Input workbook not found: {input_path}"
        )
    input_df = pd.read_excel(
        input_path, sheet_name=sheet_name,
    )
    output_df = estimate_dataframe(input_df)
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )
    with pd.ExcelWriter(
        output_path, 
        engine="openpyxl",
    ) as writer: 
        output_df.to_excel(
            writer, sheet_name="Thermo Estimates", index=False,
        )
    return output_path