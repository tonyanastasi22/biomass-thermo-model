"""
Utilities for parsing chemical formulas and calcualting molar mass.

Examples: 
---------
parse_formula("C6H12O6")
parse_formula("Ca3(PO4)2")
molar_mass("C6H12O6")
"""
from typing import Dict, Optional, Tuple
from collections import defaultdict
import re

ATOMIC_WEIGHTS = {
    "H": 1.00794, "C": 12.011, "O": 15.999, "N": 14.007, "S": 32.065
}
def _merge_counts(a: Dict[str, float], b: Dict[str, float], scale: float=1.0) -> None:
    """Merge element counts from dictionary b into dictionary a.""" 
    for k, v in b.items(): 
        a[k] += v*scale

def _parse_number(s: str, i: int) -> Tuple[float, int]: 
    """Reads an optional numeric multiplier staring at i, default 1."""
    m = re.match(r"(\d+(?:\.\d+)?)", s[i:])
    if m: 
        val = float(m.group(1))
        return val, i + len(m.group(1))
    return 1.0, i

def _parse_segment(formula: str, i: int=0) -> Tuple[Dict[str, float], int]: 
    """
    Recursively parse a chemical formula segment.

    Parameters
    ----------
    formula : str
        Chemical formula string.
    i : int
        Starting index.
    
    Returns
    -------
    counts : dict  
        Element counts.
    i : int
        Next index after parsing.
    """
    counts: Dict[str, float] = defaultdict(float)
    n = len(formula)
    while i < n: 
        ch = formula[i]
        if ch == '(': 
            inner, j = _parse_segment(formula, i+1)
            i = j
            mult, i = _parse_number(formula, i)
            _merge_counts(counts, inner, mult)
        elif ch == ')': 
            return counts, i+1
        elif ch.isupper(): 
            j = i + 1
            if j < n and formula[j].islower(): 
                j += 1
            elem = formula[i:j]
            mult, j2 = _parse_number(formula, j)

            counts[elem] += mult
            i = j2
        elif ch.isdigit(): 
            raise ValueError(f"Unexpected number at position {i} in {formula!r}")
        else: 
            raise ValueError(f"Unexpected character {ch!r} at position {i} in {formula!r}")

    return counts, i



def parse_formula(formula: str) -> Dict[str, float]: 
    """
    Parse a chemical formula into element counts. 
    Supports:
    - basic formulas: C6H12O6
    - parantheses: Ca3(PO4)2
    - hydrates using · or . : CuSO4·5H2O

    Parameters 
    ---------
    formula : str
        Chemical formula.

    Returns
    -------
    dict 
        Element counts.
    """
    if not formula or not isinstance(formula, str): 
        raise ValueError("Formula must be a non-empty string")
    parts = formula.split("·")
    total: Dict[str, float] = defaultdict(float)

    for part in parts: 
        part = part.strip()
        if not part: 
            continue
        leading_mult = 1.0
        m = re.match(r"^(\d+(?:\.\d+)?)(.*)$", part)
        if m: 
            leading_mult = float(m.group(1))
            seg = m.group(2)
        else: 
            seg = part
        counts, idx = _parse_segment(seg, 0)
        if idx !=len(seg): 
            rest = seg[idx:]
            raise ValueError(f"Unparsed tail {rest!r} in segment {seg!r}")
        
        _merge_counts(total, counts, leading_mult)

    out = {}
    for k, v in total.items(): 
        out[k] = int(v) if abs(v-round(v)) < 1e-12 else v
    return out

def molar_mass(formula: str, weights: Optional[Dict[str, float]] = None) -> float: 
    """
    Compute molar mass (g/mol).
    
    Parameters
    ----------
    formula : str
        Chemical formula.
    weights : dict, optional
        Atomic weights. Defaults to ATOMIC_WEIGHTS.
    
    Returns
    -------
    float 
        Molar mass in g/mol.
    """
    weights=weights or ATOMIC_WEIGHTS
    counts = parse_formula(formula)
    mm = 0.0
    for el, qty in counts.items(): 
        if el not in weights: 
            raise KeyError(f"Atomic weight for element {el!r} not found.")
        mm += weights[el] * qty
    return mm