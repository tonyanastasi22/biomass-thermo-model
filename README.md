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
