"""Galois theory, field extensions and polynomial roots."""

from __future__ import annotations

from typing import Any

import sympy as sp


def roots_of_polynomial(expr: Any, var: str = "x") -> list[Any]:
    x = sp.Symbol(var)
    poly = sp.Poly(sp.sympify(expr), x)
    return [complex(r) for r in sp.nroots(poly)]


def factor_polynomial(expr: Any, var: str = "x", domain: str = "QQ") -> Any:
    x = sp.Symbol(var)
    return sp.factor(sp.sympify(expr), domain=domain) if False else sp.factor(sp.Poly(sp.sympify(expr), x, domain=domain))


def is_irreducible(expr: Any, var: str = "x") -> bool:
    x = sp.Symbol(var)
    return bool(sp.Poly(sp.sympify(expr), x, domain="QQ").is_irreducible)


def minimal_polynomial(alpha: Any, var: str = "x") -> Any:
    """Minimal polynomial of an algebraic number over Q."""
    x = sp.Symbol(var)
    return sp.minimal_polynomial(sp.sympify(alpha), x)


def field_degree(expr: Any, var: str = "x") -> int:
    """[Q(root) : Q] = degree of the minimal polynomial of a root of expr."""
    x = sp.Symbol(var)
    poly = sp.Poly(sp.sympify(expr), x, domain="QQ")
    factors = sp.factor_list(poly)
    # degree of the irreducible factor
    for fac in factors[1]:
        if fac[0].is_irreducible:
            return int(fac[0].degree())
    return int(poly.degree())


def galois_group(expr: Any, var: str = "x") -> Any:
    x = sp.Symbol(var)
    poly = sp.Poly(sp.sympify(expr), x)
    return sp.galois_group(poly, by_name=True)


def splitting_field_degree(expr: Any, var: str = "x") -> int:
    """Degree of the splitting field over Q (best-effort via factorization)."""
    x = sp.Symbol(var)
    poly = sp.Poly(sp.sympify(expr), x, domain="QQ")
    # upper bound: product of distinct irreducible factor degrees
    factors = sp.factor_list(poly)
    deg = 1
    for fac, mult in factors[1]:
        deg *= int(fac.degree())
    return deg


__all__ = [
    "roots_of_polynomial", "factor_polynomial", "is_irreducible",
    "minimal_polynomial", "field_degree", "galois_group", "splitting_field_degree",
]
