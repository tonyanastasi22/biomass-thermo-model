# Model Purpose
This repository provides a lightweight, composition-driven model for estimating thermodynamic properties of CHO-based organic compounds. 
It supports batch estimation of $\Delta H_C$, $\Delta G_C$, $\Delta H_F$, $\Delta G_F$, $\Delta S_F$ and $S_0$ directly from chemical formulas, with special focus on biomass and lignocellulosic components.

## How it works
  - $\Delta H_C$ estimated using a linear regression model based on molar oxygen requirement
  - $\Delta G_C$, $\Delta H_F$ and $\Delta G_F$ are estimated via empirical regressions on elemental compositions
  - $\Delta S_F$ and $S_0$ are derived from $\Delta H_F$ and $\Delta G_F$ with adjustments for elemental entropy contributions

## Limitations
  - Only accounts for CxHyOz compounds
  - Entropy predictions are sensitive to small errors in $\Delta H_F$ and $\Delta G_F$
  - The model is not recommended for compounds with $\nu O_2$ (oxygen requirements) =< 0.5
  - Predictions are fitted to standard heating values, accuracy may decrease for highly oxygenated or nitrogen-containing compounds

## Recommendation
Use this model for rapid screening or parameter estimation when standard thermodynamic data are unavailable. 
For final analyses or detailed modeling, supplement with tabulated or experimentally validated values where possible. 

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
