"""Multi-precision decimal floating-point physics integration."""

from __future__ import annotations

import math
from decimal import Decimal, getcontext

import mpmath


class ArbitraryPrecision:
    """mpmath-backed high-precision physics computations."""

    @staticmethod
    def set_precision(digits: int = 50) -> None:
        getcontext().prec = digits
        mpmath.mp.dps = digits

    @staticmethod
    def exp_series(x: float, terms: int = 30) -> mpmath.mpf:
        ArbitraryPrecision.set_precision(50)
        s = mpmath.mpf(0)
        term = mpmath.mpf(1)
        for k in range(terms):
            s += term
            term *= mpmath.mpf(x) / (k + 1)
        return s

    @staticmethod
    def integrate_quadrature(f, a: float, b: float, max_degree: int = 11) -> mpmath.mpf:
        """Gauss-Legendre quadrature at high precision."""
        nodes, weights = mpmath.gauss_quadrature(max_degree)
        result = mpmath.mpf(0)
        half = (mpmath.mpf(b) - mpmath.mpf(a)) / 2
        mid = (mpmath.mpf(a) + mpmath.mpf(b)) / 2
        for x, w in zip(nodes, weights):
            result += mpmath.mpf(w) * f(mid + half * x)
        return half * result

    @staticmethod
    def constant_to_precision(name: str, digits: int = 50) -> mpmath.mpf:
        ArbitraryPrecision.set_precision(digits)
        table = {"pi": mpmath.pi, "e": mpmath.e, "phi": (1 + mpmath.sqrt(5)) / 2}
        return table[name]
