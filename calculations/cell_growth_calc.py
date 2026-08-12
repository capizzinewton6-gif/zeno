"""Doubling time, optical density, and dilution math."""
from __future__ import annotations

import math


def doubling_time(n0, n_t, t):
    if n0 <= 0 or n_t <= 0 or t <= 0:
        raise ValueError("All inputs must be positive")
    return t * math.log(2) / math.log(n_t / n0)


def growth_rate(n0, n_t, t):
    return math.log(n_t / n0) / t


def od_to_cells(od600, cells_per_ml_per_od=1e9):
    return od600 * cells_per_ml_per_od


def serial_dilution(initial_conc, dilution_factor, steps):
    """Return concentration after each serial dilution step."""
    c = initial_conc
    series = [c]
    for _ in range(steps):
        c /= dilution_factor
        series.append(c)
    return series


def molarity(moles, liters):
    if liters <= 0:
        raise ValueError("Volume must be > 0")
    return moles / liters


def cfu_per_ml(colonies, dilution_factor, volume_plated):
    return colonies * dilution_factor / volume_plated
