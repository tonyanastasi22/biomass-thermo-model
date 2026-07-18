# CHO Thermodynamic Property Estimator

This tool estimates combustion and formation properties for
carbon-containing CHO compounds using a composition-based model. 

## Installation (first time only)

1. Install Python 3.11+
2. Double-click setup.bat
3. Wait until installation finishes.

## Input Workbook

Place 'compounds.xlsx' in the 'input' folder. 

Required columns: 
- Compound
- Formula

## Normal use

1. Open 'input/compounds.xlsx'.
2. Enter compound names and formulas.
3. Save and close Excel.
4. Double-click 'run_estimator.bat'
5. Open 'output/thermo_results.xlsx'.

## Scope

This model is intended for early-stage thermodynamic screening. 
Supports: 
- CHO compounds
- Neutral molecules
Not yet supported: 
- Nitrogen
- Sulfur
- Radicals
- Ions
- Phase effects

## Troubleshooting

If Windows prevents setup.bat or run_estimator.bat from opening: 
1. Right click on the .bat file
2. Select Properties
3. If the Unblock checkbox appears at the bottom of the window, check it.
4. Click Apply and OK.
5. Try running the file again.

## Testing

Tested with: 
- Windows 11
- Python 3.13.2

## Citation

Based on work of Anastasi, A. et al in ESCAPE36 Proceedings.
"Estimation of Thermodynamic Properties for Cellulosic Biomass-Derived Compounds: Applications to Heat and Work Balances in Process Simulation"