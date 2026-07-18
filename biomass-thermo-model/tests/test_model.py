import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"

if str(SRC_DIR) not in sys.path: 
    sys.path.insert(0, str(SRC_DIR))

from cho_thermo import estimate_properties

def test_furfural_runs(): 
    result = estimate_properties("C5H4O2")

    assert result["C"] == 5
    assert result["H"] == 4
    assert result["O"] == 2
    assert result["Oxygen Demand (mol O2/mol)"] > 0

def test_rejects_nitrogen(): 
    with pytest.raises(ValueError): 
        estimate_properties("C5H5NO2")
