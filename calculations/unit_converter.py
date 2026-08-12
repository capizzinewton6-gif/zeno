"""Biological unit conversions (uM, CFU/mL, kDa, bp)."""
from __future__ import annotations

import math

AVOGADRO = 6.02214076e23


def molar_to_mg_ml(molarity_M, mw_g_mol):
    # mol/L * g/mol = g/L = mg/mL (1 g/L == 1 mg/mL)
    return molarity_M * mw_g_mol


def mg_ml_to_molar(mg_ml, mw_g_mol):
    if mw_g_mol == 0:
        raise ValueError("MW must be > 0")
    # mg/mL == g/L == mol/L * MW  ->  M = mg_ml / mw
    return mg_ml / mw_g_mol


def bp_to_daltons(bp, double_stranded=True):
    return bp * (660.0 if double_stranded else 330.0)


def kda_to_daltons(kda):
    return kda * 1000.0


def molecules_per_cell(molarity_uM, cell_volume_pl=1.0):
    """Estimate molecule count per cell given intracellular concentration."""
    molarity_M = molarity_uM * 1e-6
    volume_L = cell_volume_pl * 1e-12
    return molarity_M * AVOGADRO * volume_L


def dilute(stock_conc, stock_vol, final_conc):
    """Volume of diluent needed to reach final concentration."""
    if final_conc <= 0:
        raise ValueError("Final concentration must be > 0")
    if final_conc > stock_conc:
        raise ValueError("Final concentration exceeds stock")
    final_vol = stock_conc * stock_vol / final_conc
    return final_vol - stock_vol


def moles_from_mass(mass_g, mw_g_mol):
    if mw_g_mol == 0:
        raise ValueError("MW must be > 0")
    return mass_g / mw_g_mol
