"""Metric tensors, Christoffel symbols, Riemann/Ricci tensors, and Ricci scalar."""

from __future__ import annotations

import numpy as np
import sympy as sp


class TensorCalculus:
    """Symbolic differential-geometry computations on a metric tensor."""

    @staticmethod
    def christoffel_symbols(metric: sp.Matrix, coords: list[sp.Symbol]) -> list[sp.MutableDenseNDimArray]:
        """Gamma^a_{bc} from the metric and its derivatives."""
        n = len(coords)
        inv = metric.inv()
        gamma = np.zeros((n, n, n), dtype=object)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    val = 0
                    for d in range(n):
                        val += inv[a, d] * (sp.diff(metric[d, b], coords[c]) +
                                             sp.diff(metric[d, c], coords[b]) -
                                             sp.diff(metric[b, c], coords[d]))
                    gamma[a, b, c] = sp.simplify(val / 2)
        return gamma

    @staticmethod
    def riemann_tensor(metric: sp.Matrix, coords: list[sp.Symbol]) -> np.ndarray:
        """R^a_{bcd}. Computed from Christoffel symbols."""
        n = len(coords)
        gamma = TensorCalculus.christoffel_symbols(metric, coords)
        R = np.zeros((n, n, n, n), dtype=object)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        term = sp.diff(gamma[a, b, d], coords[c]) - sp.diff(gamma[a, b, c], coords[d])
                        for e in range(n):
                            term += gamma[a, c, e] * gamma[e, b, d] - gamma[a, d, e] * gamma[e, b, c]
                        R[a, b, c, d] = sp.simplify(term)
        return R

    @staticmethod
    def ricci_tensor(metric: sp.Matrix, coords: list[sp.Symbol]) -> sp.Matrix:
        """R_ab = R^c_{acb}."""
        n = len(coords)
        R = TensorCalculus.riemann_tensor(metric, coords)
        Ric = sp.zeros(n, n)
        for a in range(n):
            for b in range(n):
                val = 0
                for c in range(n):
                    val += R[c, a, c, b]
                Ric[a, b] = sp.simplify(val)
        return Ric

    @staticmethod
    def ricci_scalar(metric: sp.Matrix, coords: list[sp.Symbol]) -> sp.Expr:
        """R = g^{ab} R_ab."""
        n = len(coords)
        inv = metric.inv()
        Ric = TensorCalculus.ricci_tensor(metric, coords)
        R = 0
        for a in range(n):
            for b in range(n):
                R += inv[a, b] * Ric[a, b]
        return sp.simplify(R)

    @staticmethod
    def flrw_metric() -> tuple[sp.Matrix, list[sp.Symbol]]:
        """Spatially flat FLRW metric in comoving coordinates."""
        t, r, theta, phi = sp.symbols("t r theta phi")
        a = sp.Function("a")(t)
        g = sp.diag(-1, a ** 2, a ** 2 * r ** 2, a ** 2 * r ** 2 * sp.sin(theta) ** 2)
        return g, [t, r, theta, phi]


TENSOR = TensorCalculus()
