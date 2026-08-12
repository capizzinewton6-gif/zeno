"""Real, complex, functional and harmonic analysis.

Backed by SymPy for symbolic work and mpmath for high-precision numerics.
"""

from __future__ import annotations

from typing import Any

import sympy as sp
import mpmath


def _x():
    return sp.Symbol("x")


def limit(expr: Any, var: str = "x", to: Any = 0, direction: str = "+") -> Any:
    v = sp.Symbol(var)
    return sp.limit(sp.sympify(expr), v, to, dir=direction)


def derivative(expr: Any, var: str = "x", order: int = 1) -> Any:
    v = sp.Symbol(var)
    return sp.diff(sp.sympify(expr), v, order)


def integrate(expr: Any, var: str = "x", *bounds: Any) -> Any:
    """Indefinite or definite integration."""
    v = sp.Symbol(var)
    if bounds:
        return sp.integrate(sp.sympify(expr), (v, *bounds))
    return sp.integrate(sp.sympify(expr), v)


def series(expr: Any, var: str = "x", around: Any = 0, n: int = 6) -> Any:
    v = sp.Symbol(var)
    return sp.series(sp.sympify(expr), v, around, n)


def taylor_coefficients(expr: Any, var: str = "x", n: int = 5) -> list[Any]:
    f = sp.sympify(expr)
    v = sp.Symbol(var)
    return [sp.diff(f, v, k).subs(v, 0) / sp.factorial(k) for k in range(n)]


def fourier_series(expr: Any, var: str = "x", n: int = 5) -> dict[str, Any]:
    """Compute the first n Fourier coefficients of a 2π-periodic function."""
    v = sp.Symbol(var)
    f = sp.sympify(expr)
    a0 = (1 / sp.pi) * sp.integrate(f, (v, -sp.pi, sp.pi))
    coefs = {"a0": sp.simplify(a0)}
    for k in range(1, n + 1):
        ak = (1 / sp.pi) * sp.integrate(f * sp.cos(k * v), (v, -sp.pi, sp.pi))
        bk = (1 / sp.pi) * sp.integrate(f * sp.sin(k * v), (v, -sp.pi, sp.pi))
        coefs[f"a{k}"] = sp.simplify(ak)
        coefs[f"b{k}"] = sp.simplify(bk)
    return coefs


def is_continuous_at(expr: Any, var: str = "x", point: Any = 0) -> bool:
    v = sp.Symbol(var)
    try:
        left = sp.limit(sp.sympify(expr), v, point, "-")
        right = sp.limit(sp.sympify(expr), v, point, "+")
        val = sp.sympify(expr).subs(v, point)
        return bool(sp.simplify(left - right) == 0 and sp.simplify(right - val) == 0)
    except Exception:
        return False


def residue(expr: Any, var: str = "z", point: Any = 0) -> Any:
    """Residue of a complex function at a point (coefficient of (z-z0)^-1)."""
    v = sp.Symbol(var)
    return sp.residue(sp.sympify(expr), v, point)


def evaluate_high_precision(expr: Any, subs: dict[str, Any] | None = None, digits: int = 50) -> str:
    """Evaluate an expression to ``digits`` decimal places using mpmath."""
    mpmath.mp.dps = digits
    f = sp.lambdify(list((subs or {}).keys()) or ["x"], sp.sympify(expr), modules="mpmath")
    if subs:
        return mpmath.nstr(f(*subs.values()), digits)
    return mpmath.nstr(f(0), digits)


__all__ = [
    "limit", "derivative", "integrate", "series", "taylor_coefficients",
    "fourier_series", "is_continuous_at", "residue", "evaluate_high_precision",
]
