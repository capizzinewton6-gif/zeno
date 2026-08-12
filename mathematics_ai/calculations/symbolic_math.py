"""Symbolic integration, differentiation, and limits via SymPy.

A unified calculation front-end that wraps SymPy with friendly defaults and
returns plain Python/SymPy objects suitable for serialization.
"""

from __future__ import annotations

from typing import Any

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)


def _parse(expr: Any) -> sp.Expr:
    """Parse a string expression, tolerating ``^`` and implicit multiplication."""
    if isinstance(expr, str):
        return parse_expr(expr, transformations=_TRANSFORMATIONS)
    return sp.sympify(expr)


def _parse_equation(expr: Any) -> sp.Expr:
    """Parse an expression that may be an equation ``lhs = rhs``."""
    if isinstance(expr, str) and "=" in expr and "==" not in expr:
        lhs, rhs = expr.split("=", 1)
        return sp.Eq(_parse(lhs), _parse(rhs))
    return _parse(expr)


def _symbol(var: str) -> sp.Symbol:
    return sp.Symbol(var)


def differentiate(expr: Any, var: str = "x", order: int = 1) -> Any:
    return sp.diff(_parse(expr), _symbol(var), order)


def integrate(expr: Any, var: str = "x", *bounds: Any) -> Any:
    v = _symbol(var)
    if bounds:
        return sp.integrate(_parse(expr), (v, *bounds))
    return sp.integrate(_parse(expr), v)


def limit(expr: Any, var: str = "x", to: Any = 0, direction: str = "+") -> Any:
    return sp.limit(_parse(expr), _symbol(var), to, dir=direction)


def series_expansion(expr: Any, var: str = "x", around: Any = 0, n: int = 6) -> Any:
    return sp.series(_parse(expr), _symbol(var), around, n)


def simplify(expr: Any) -> Any:
    return sp.simplify(_parse(expr))


def solve(expr: Any, var: str = "x") -> list[Any]:
    parsed = _parse_equation(expr)
    sols = sp.solve(parsed, _symbol(var))
    return list(sols) if isinstance(sols, list) else [sols]


def solve_system(equations: list[Any], variables: list[str]) -> list[dict[str, Any]]:
    vs = sp.symbols(",".join(variables))
    if not isinstance(vs, tuple):
        vs = (vs,)
    sols = sp.solve([_parse(e) for e in equations], list(vs), dict=True)
    return sols


def partial_fractions(expr: Any, var: str = "x") -> Any:
    return sp.apart(_parse(expr), _symbol(var))


def taylor_series(expr: Any, var: str = "x", n: int = 6) -> Any:
    return sp.series(_parse(expr), _symbol(var), 0, n)


def laplace_transform(expr: Any, var: str = "t", s: str = "s") -> Any:
    return sp.laplace_transform(_parse(expr), _symbol(var), _symbol(s))[0]


def inverse_laplace_transform(expr: Any, s: str = "s", var: str = "t") -> Any:
    return sp.inverse_laplace_transform(_parse(expr), _symbol(s), _symbol(var))[0]


def fourier_transform(expr: Any, var: str = "x", k: str = "k") -> Any:
    return sp.fourier_transform(_parse(expr), _symbol(var), _symbol(k))


__all__ = [
    "differentiate", "integrate", "limit", "series_expansion", "simplify",
    "solve", "solve_system", "partial_fractions", "taylor_series",
    "laplace_transform", "inverse_laplace_transform", "fourier_transform",
]
