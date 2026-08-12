"""Confirm correct classical or non-relativistic limit behaviors."""

from __future__ import annotations

import sympy as sp


class AsymptoticVerifier:
    """Check that a relativistic/quantum expression reduces to the expected limit."""

    @staticmethod
    def nonrelativistic_limit(rel_expr: sp.Expr, v: sp.Symbol, expected: sp.Expr) -> dict:
        """Expand rel_expr in v/c -> 0 and compare leading order to expected."""
        series = sp.series(rel_expr, v, 0, 2).removeO()
        diff = sp.simplify(series - expected)
        return {"series": str(series), "expected": str(expected), "matches": diff == 0}

    @staticmethod
    def classical_limit(hbar_expr: sp.Expr, hbar: sp.Symbol, expected: sp.Expr) -> dict:
        """Expand an expression in hbar -> 0 and compare to the classical result."""
        series = sp.series(hbar_expr, hbar, 0, 1).removeO()
        diff = sp.simplify(series - expected)
        return {"series": str(series), "expected": str(expected), "matches": diff == 0}

    @staticmethod
    def high_temperature_limit(expr: sp.Expr, T: sp.Symbol, expected_leading: sp.Expr) -> dict:
        series = sp.series(expr, 1 / T, 0, 1).removeO()
        diff = sp.simplify(series - expected_leading)
        return {"series": str(series), "expected": str(expected_leading), "matches": diff == 0}
