"""Tensor operations, Christoffel symbols and differential forms via SymPy."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _coords(names: str):
    return sp.symbols(names)


def tensor_product(a: list[Any], b: list[Any]) -> list[Any]:
    """Outer product of two 1-index lists."""
    return [[sp.sympify(x) * sp.sympify(y) for y in b] for x in a]


def contract(tensor: list[list[Any]], i: int, j: int) -> list[Any]:
    """Contract indices i and j of a rank-2 tensor."""
    T = sp.Matrix(tensor)
    return sp.simplify(T.trace()).tolist() if i == 0 and j == 1 else T.row(i).dot(T.col(j))


def riemann_tensor(metric: list[list[Any]], coords: str = "t,r,theta,phi") -> list[list[list[list[Any]]]]:
    """Riemann curvature tensor R^rho_sig mu nu from the metric."""
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    n = len(cs)
    g = sp.Matrix([[sp.sympify(metric[i][j]) for j in range(n)] for i in range(n)])
    g_inv = g.inv()
    # Christoffel symbols Gamma^k_ij
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
    # R^rho_sig mu nu = d_mu Gamma^rho_nu sig - d_nu Gamma^rho_mu sig
    #                 + Gamma^rho_mu a Gamma^a_nu sig - Gamma^rho_nu a Gamma^a_mu sig
    R = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    val = (sp.diff(Gamma[rho][nu][sig], cs[mu])
                           - sp.diff(Gamma[rho][mu][sig], cs[nu]))
                    for a in range(n):
                        val += (Gamma[rho][mu][a] * Gamma[a][nu][sig]
                                - Gamma[rho][nu][a] * Gamma[a][mu][sig])
                    R[rho][sig][mu][nu] = sp.simplify(val)
    return R


def ricci_tensor(metric: list[list[Any]], coords: str = "t,r,theta,phi") -> list[list[Any]]:
    """Ricci tensor R_sigma mu = R^rho_sig rho mu."""
    R = riemann_tensor(metric, coords)
    n = len(R)
    Ricci = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    for sig in range(n):
        for mu in range(n):
            s = 0
            for rho in range(n):
                s += R[rho][sig][rho][mu]
            Ricci[sig][mu] = sp.simplify(s)
    return Ricci


def ricci_scalar(metric: list[list[Any]], coords: str = "t,r,theta,phi") -> Any:
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    n = len(cs)
    g = sp.Matrix([[sp.sympify(metric[i][j]) for j in range(n)] for i in range(n)])
    g_inv = g.inv()
    Ricci = ricci_tensor(metric, coords)
    R = 0
    for i in range(n):
        for j in range(n):
            R += g_inv[i, j] * Ricci[i][j]
    return sp.simplify(R)


def exterior_derivative(form: list[Any], coords: str = "x,y,z") -> list[Any]:
    """Exterior derivative of a 1-form: (dω)_ij = ∂_i ω_j - ∂_j ω_i."""
    cs = _coords(coords)
    if isinstance(cs, sp.Symbol):
        cs = (cs,)
    f = [sp.sympify(v) for v in form]
    n = len(f)
    return [[sp.diff(f[j], cs[i]) - sp.diff(f[i], cs[j]) for j in range(n)] for i in range(n)]


__all__ = [
    "tensor_product", "contract", "riemann_tensor", "ricci_tensor",
    "ricci_scalar", "exterior_derivative",
]
