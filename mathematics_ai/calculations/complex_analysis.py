"""Residue calculus, contour integration and conformal mappings."""

from __future__ import annotations

from typing import Any

import sympy as sp
import numpy as np


def residue(expr: Any, var: str = "z", point: Any = 0) -> Any:
    z = sp.Symbol(var)
    return sp.residue(sp.sympify(expr), z, point)


def poles(expr: Any, var: str = "z") -> list[Any]:
    """Find poles of a rational function."""
    z = sp.Symbol(var)
    f = sp.sympify(expr)
    rat = sp.together(f)
    num, den = sp.fraction(rat)
    den_poly = sp.Poly(den, z)
    return [complex(r) for r in sp.nroots(den_poly)]


def contour_integral_residues(expr: Any, var: str = "z") -> Any:
    """Sum of residues inside a contour = 2πi Σ residues (all finite poles)."""
    z = sp.Symbol(var)
    f = sp.sympify(expr)
    rat = sp.together(f)
    _, den = sp.fraction(rat)
    den_poly = sp.Poly(den, z)
    roots = sp.nroots(den_poly)
    total = sum(complex(sp.residue(f, z, sp.nsimplify(r))) for r in roots)
    return 2 * sp.pi * sp.I * total


def conformal_map_check(f: Any, var: str = "z") -> bool:
    """A function is conformal where it is analytic and f'(z) ≠ 0."""
    z = sp.Symbol(var)
    deriv = sp.diff(sp.sympify(f), z)
    return deriv != 0


def laurent_series(expr: Any, var: str = "z", around: Any = 0, n: int = 4) -> Any:
    """Laurent series expansion around a point."""
    z = sp.Symbol(var)
    return sp.series(sp.sympify(expr), z, around, n)


def evaluate_on_contour(expr: Any, center: complex = 0, radius: float = 1.0, n: int = 1000) -> complex:
    """Numerically integrate f(z) dz around |z-c| = radius."""
    z = sp.Symbol("z")
    f = sp.lambdify(z, sp.sympify(expr), "numpy")
    theta = np.linspace(0, 2 * np.pi, n)
    zs = center + radius * np.exp(1j * theta)
    dz = np.diff(zs)
    vals = f(zs[:-1])
    return complex(np.sum(vals * dz))


__all__ = [
    "residue", "poles", "contour_integral_residues", "conformal_map_check",
    "laurent_series", "evaluate_on_contour",
]
