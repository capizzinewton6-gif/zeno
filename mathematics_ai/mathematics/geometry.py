"""Differential, algebraic, Riemannian and Euclidean geometry."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _coords(names: str):
    return sp.symbols(names)


def euclidean_distance(p1: tuple[Any, ...], p2: tuple[Any, ...]) -> Any:
    return sp.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def triangle_area_heron(a: Any, b: Any, c: Any) -> Any:
    s = (a + b + c) / 2
    return sp.sqrt(s * (s - a) * (s - b) * (s - c))


def gradient(expr: Any, coords: str = "x,y,z") -> list[Any]:
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    f = sp.sympify(expr)
    return [sp.diff(f, c) for c in cs]


def divergence(field: list[Any], coords: str = "x,y,z") -> Any:
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    field = [sp.sympify(v) for v in field]
    return sum(sp.diff(v, c) for v, c in zip(field, cs))


def curl(field: list[Any], coords: str = "x,y,z") -> list[Any]:
    """Curl of a 3-vector field."""
    x, y, z = _coords("x,y,z")
    F = [sp.sympify(v) for v in field]
    return [
        sp.diff(F[2], y) - sp.diff(F[1], z),
        sp.diff(F[0], z) - sp.diff(F[2], x),
        sp.diff(F[1], x) - sp.diff(F[0], y),
    ]


def laplacian(expr: Any, coords: str = "x,y,z") -> Any:
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    f = sp.sympify(expr)
    return sum(sp.diff(f, c, 2) for c in cs)


def christoffel_symbols(metric: list[list[Any]], coords: str = "t,r,theta,phi") -> list[list[list[Any]]]:
    """Christoffel symbols Γ^k_ij from a metric tensor g_ij."""
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    n = len(cs)
    g = sp.Matrix([[sp.sympify(metric[i][j]) for j in range(n)] for i in range(n)])
    g_inv = g.inv()
    Gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.Integer(0)
                for l in range(n):
                    s += sp.Rational(1, 2) * g_inv[k, l] * (
                        sp.diff(g[l, i], cs[j]) + sp.diff(g[l, j], cs[i]) - sp.diff(g[i, j], cs[l])
                    )
                Gamma[k][i][j] = sp.simplify(s)
    return Gamma


def arc_length(expr_x: Any, expr_y: Any, var: str = "t", a: Any = 0, b: Any = 1) -> Any:
    """Arc length of a parametric curve (x(t), y(t)) on [a,b]."""
    t = sp.Symbol(var)
    dx, dy = sp.diff(sp.sympify(expr_x), t), sp.diff(sp.sympify(expr_y), t)
    return sp.integrate(sp.sqrt(dx ** 2 + dy ** 2), (t, a, b))


def curvature_2d(expr_x: Any, expr_y: Any, var: str = "t") -> Any:
    """Signed curvature κ = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)."""
    t = sp.Symbol(var)
    x = sp.sympify(expr_x); y = sp.sympify(expr_y)
    xp, yp = sp.diff(x, t), sp.diff(y, t)
    xpp, ypp = sp.diff(x, t, 2), sp.diff(y, t, 2)
    return sp.simplify((xp * ypp - yp * xpp) / (xp ** 2 + yp ** 2) ** sp.Rational(3, 2))


__all__ = [
    "euclidean_distance", "triangle_area_heron", "gradient", "divergence",
    "curl", "laplacian", "christoffel_symbols", "arc_length", "curvature_2d",
]
