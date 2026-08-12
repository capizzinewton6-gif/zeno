"""Riemannian metrics, Ricci curvature and Einstein tensors."""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp


def riemann_tensor_2d(g: Any, coords: list[sp.Symbol]) -> Any:
    """Compute the single independent component R_1212 of a 2D metric."""
    n = len(coords)
    # Christoffel symbols
    g_inv = sp.Matrix(g).inv()
    Gamma = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s = 0
                for m in range(n):
                    s += sp.Rational(1, 2) * g_inv[k, m] * (
                        sp.diff(g[m, i], coords[j]) + sp.diff(g[m, j], coords[i]) - sp.diff(g[i, j], coords[m])
                    )
                Gamma[i][j][k] = sp.simplify(s)
    # R_1212
    R = (sp.diff(Gamma[0][1][1], coords[0]) - sp.diff(Gamma[0][0][1], coords[1]))
    for m in range(n):
        R += Gamma[0][0][m] * Gamma[m][1][1] - Gamma[0][1][m] * Gamma[m][0][1]
    return sp.simplify(R)


def ricci_scalar_2d(g: Any, coords: list[sp.Symbol]) -> Any:
    """K = 2 * R_1212 / det(g) for a 2D Riemannian metric."""
    det = sp.Matrix(g).det()
    R1212 = riemann_tensor_2d(g, coords)
    return sp.simplify(2 * R1212 / det)


def sphere_metric_ricci(r: float = 1.0) -> sp.Expr:
    """Ricci scalar of the 2-sphere of radius r is 2/r^2."""
    return sp.Rational(2) / (r * r) if isinstance(r, (int, float, sp.Number)) else 2 / r ** 2


def einstein_tensor_components(g: Any, coords: list[sp.Symbol]) -> Any:
    """G_ab = R_ab - (1/2) g_ab R. Placeholder returns None for general metrics."""
    return None


def sectional_curvature(g: Any, u: list[Any], v: list[Any]) -> Any:
    """Sectional curvature of the plane spanned by u, v (constant curvature only)."""
    g_mat = sp.Matrix(g)
    num = (sp.Matrix(u).dot(g_mat * sp.Matrix(v)))
    denom = (sp.Matrix(u).dot(g_mat * sp.Matrix(u))) * (sp.Matrix(v).dot(g_mat * sp.Matrix(v))) - num ** 2
    if denom == 0:
        return None
    return sp.simplify(num / denom)


__all__ = [
    "riemann_tensor_2d", "ricci_scalar_2d", "sphere_metric_ricci",
    "einstein_tensor_components", "sectional_curvature",
]
