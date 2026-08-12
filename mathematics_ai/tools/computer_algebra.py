"""Computer Algebra System integration (SymPy, and adapters for Sage/Maxima).

In this environment SymPy is the default CAS. The adapter exposes a uniform
``CAS`` object so callers can request simplification, factorization, solving,
and series expansion without binding to SymPy internals.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


class CAS:
    """Uniform computer-algebra facade (SymPy-backed by default)."""

    def __init__(self, backend: str = "sympy") -> None:
        if backend != "sympy":
            raise NotImplementedError("Only the SymPy backend is available in this environment.")
        self.backend = backend

    @staticmethod
    def parse(expr: str) -> sp.Expr:
        return sp.sympify(expr)

    @staticmethod
    def simplify(expr: Any) -> Any:
        return sp.simplify(sp.sympify(expr))

    @staticmethod
    def factor(expr: Any, var: str = "x") -> Any:
        x = sp.Symbol(var)
        return sp.factor(sp.sympify(expr), x)

    @staticmethod
    def expand(expr: Any) -> Any:
        return sp.expand(sp.sympify(expr))

    @staticmethod
    def solve(expr: Any, var: str = "x") -> list[Any]:
        x = sp.Symbol(var)
        sols = sp.solve(sp.sympify(expr), x)
        return list(sols) if isinstance(sols, list) else [sols]

    @staticmethod
    def differentiate(expr: Any, var: str = "x") -> Any:
        return sp.diff(sp.sympify(expr), sp.Symbol(var))

    @staticmethod
    def integrate(expr: Any, var: str = "x", *bounds: Any) -> Any:
        x = sp.Symbol(var)
        if bounds:
            return sp.integrate(sp.sympify(expr), (x, *bounds))
        return sp.integrate(sp.sympify(expr), x)

    @staticmethod
    def series(expr: Any, var: str = "x", n: int = 6) -> Any:
        return sp.series(sp.sympify(expr), sp.Symbol(var), 0, n)

    @staticmethod
    def matrix(rows: list[list[Any]]) -> sp.Matrix:
        return sp.Matrix(rows)

    @staticmethod
    def to_latex(expr: Any) -> str:
        return sp.latex(sp.sympify(expr))

    @staticmethod
    def from_latex(latex_str: str) -> Any:
        try:
            from sympy.parsing.latex import parse_latex  # type: ignore
            return parse_latex(latex_str)
        except Exception:
            # Fallback: try antlr-free parsing of common forms
            return sp.sympify(latex_str.replace("\\", "").replace("frac", "Rational"))


# Module-level convenience instance
cas = CAS()


def simplify(expr: Any) -> Any:
    return cas.simplify(expr)


def solve(expr: Any, var: str = "x") -> list[Any]:
    return cas.solve(expr, var)


def integrate(expr: Any, var: str = "x", *bounds: Any) -> Any:
    return cas.integrate(expr, var, *bounds)


def to_latex(expr: Any) -> str:
    return cas.to_latex(expr)


__all__ = ["CAS", "cas", "simplify", "solve", "integrate", "to_latex"]
