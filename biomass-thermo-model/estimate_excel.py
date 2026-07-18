from pathlib import Path
import sys

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path: 
    sys.path.insert(0, str(SRC_DIR))

from cho_thermo.excel import process_excel_workbook 

INPUT_FILE = BASE_DIR / "input" / "compounds.xlsx"
OUTPUT_FILE = BASE_DIR / "output" / "thermo_results.xlsx"

if __name__ == "__main__": 
    try: 
        result_path = process_excel_workbook(
            input_file=INPUT_FILE, 
            output_file=OUTPUT_FILE,
        )

        print()
        print("Thermodynamic estimation complete.")
        print(f"Results saved to:\n{result_path}")
        
    except Exception as exc: 
        print()
        print("The estimator could not complete:")
        print(exc)
        raise SystemExit(1)
