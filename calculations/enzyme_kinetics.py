"""Michaelis-Menten and Lineweaver-Burk calculations."""
from __future__ import annotations

import math


def michaelis_menten(s, vmax, km):
    if km == 0:
        raise ValueError("Km must be > 0")
    return vmax * s / (km + s)


def lineweaver_burk(vmax, km, s_values):
    return [(1 / s, 1 / michaelis_menten(s, vmax, km)) for s in s_values]


def km_from_double_reciprocal(slope, intercept):
    """slope = Km/Vmax, intercept = 1/Vmax."""
    if intercept == 0:
        raise ValueError("Intercept must be non-zero")
    vmax = 1 / intercept
    return slope * vmax


def inhibition_type(alpha_km, alpha_vmax):
    """Classify inhibition from relative Km and Vmax changes (control=1.0)."""
    if math.isclose(alpha_vmax, 1.0, abs_tol=1e-3) and not math.isclose(alpha_km, 1.0, abs_tol=1e-3):
        return "competitive"
    if math.isclose(alpha_km, 1.0, abs_tol=1e-3) and not math.isclose(alpha_vmax, 1.0, abs_tol=1e-3):
        return "noncompetitive"
    if not math.isclose(alpha_km, 1.0, abs_tol=1e-3) and not math.isclose(alpha_vmax, 1.0, abs_tol=1e-3):
        return "mixed"
    if alpha_km == alpha_vmax:
        return "uncompetitive"
    return "unknown"


def optimize_yield(parameters, response):
    """Naive linear coefficient estimate for yield optimization."""
    import numpy as np
    if len(parameters) != len(response):
        raise ValueError("parameters and response must be equal length")
    keys = sorted(parameters.keys())
    X = np.array([[parameters[k][i] for k in keys] for i in range(len(response))], dtype=float)
    y = np.array(response, dtype=float)
    X = np.c_[np.ones(len(y)), X]
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coeffs
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {"coefficients": dict(zip(["intercept"] + keys, coeffs)), "r_squared": r2}
