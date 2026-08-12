"""High-degree polynomial and transcendental root finders."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
import sympy as sp
from scipy import optimize


def polynomial_roots(coeffs: list[float]) -> list[complex]:
    """Roots of a polynomial given by coefficients (highest degree first)."""
    return np.roots(coeffs).tolist()


def polynomial_roots_symbolic(expr: Any, var: str = "x") -> list[Any]:
    x = sp.Symbol(var)
    return sp.nroots(sp.sympify(expr))


def find_root_bisection(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def find_root_newton(f: Callable[[float], float], fp: Callable[[float], float], x0: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        d = fp(x)
        if d == 0:
            raise ZeroDivisionError("derivative zero")
        x = x - fx / d
    return x


def find_root_secant(f: Callable[[float], float], x0: float, x1: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1) < tol:
            return x1
        if f1 - f0 == 0:
            raise ZeroDivisionError("secant denominator zero")
        x0, x1 = x1, x1 - f1 * (x1 - x0) / (f1 - f0)
    return x1


def find_all_roots(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> list[float]:
    """Find all real roots of f in [a,b] by sign changes + refinement."""
    xs = np.linspace(a, b, n)
    roots = []
    for i in range(n - 1):
        if f(xs[i]) == 0:
            roots.append(float(xs[i]))
        elif f(xs[i]) * f(xs[i + 1]) < 0:
            roots.append(find_root_bisection(f, xs[i], xs[i + 1]))
    return roots


def transcendental_root(f: Callable[[float], float], x0: float) -> float:
    return float(optimize.fsolve(f, x0)[0])


__all__ = [
    "polynomial_roots", "polynomial_roots_symbolic", "find_root_bisection",
    "find_root_newton", "find_root_secant", "find_all_roots", "transcendental_root",
]
