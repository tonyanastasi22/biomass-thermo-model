# Model Purpose
This repository provides a lightweight, composition-driven model for estimating thermodynamic properties of CHO-based organic compounds. 
It supports batch estimation of ΔH_C, ΔG_C, ΔH_F, ΔG_F, ΔS_F and S0 directly from chemical formulas, with special focus on biomass and lignocellulosic components.

## How it works
  - ΔH_C estimated using a linear regression model based on molar oxygen requirement
  - ΔG_C, ΔH_F and ΔG_F are estimated via empirical regressions on elemental compositions
  - ΔS_F and S0 are derived from ΔH_F and ΔG_F with adjustments for elemental entropy contributions

## Limitations
  - Only accounts for CxHyOz compounds
  - Entropy predictions are sensitive to small errors in ΔH_F and ΔG_F
  - The model is not recommended for compounds with vO2 (oxygen requirements) =< 0.5
  - Predictions are fitted to standard heating values, accuracy may decrease for highly oxygenated or nitrogen-containing compounds

## Recommendation
Use this model for rapid screening or parameter estimation when standard thermodynamic data are unavailable. 
For final analyses or detailed modeling, supplement with tabulated or experimentally validated values where possible. 
