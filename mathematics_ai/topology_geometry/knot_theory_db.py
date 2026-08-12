"""Knot invariants (Jones, Alexander polynomials) and tables."""

from __future__ import annotations

import numpy as np
import sympy as sp

# A small table of common knots: name -> crossing number, Jones polynomial
KNOT_TABLE: list[dict[str, Any]] = [  # type: ignore[name-defined]
    {"name": "unknot", "crossing_number": 0, "jones": "1", "alexander": "1"},
    {"name": "trefoil_3_1", "crossing_number": 3, "jones": "-q^{-4} - q^{-3} + q^{-1}", "alexander": "t^2 - t + 1"},
    {"name": "figure_eight_4_1", "crossing_number": 4, "jones": "q^2 - q + 1 - q^{-1} + q^{-2}", "alexander": "-t + 3 - t^{-1}"},
    {"name": "cinquefoil_5_1", "crossing_number": 5, "jones": "-q^{-7} + q^{-6} - q^{-5} + q^{-4} + q^{-2}", "alexander": "t^4 - t^3 + t^2 - t + 1"},
    {"name": "three_twist_5_2", "crossing_number": 5, "jones": "q^{-1} + q^{-2} - 2*q^{-3} + q^{-4} - q^{-5}", "alexander": "2 t - 3 + 2 t^{-1}"},
]  # type: ignore[name-defined]

from typing import Any


def list_knots() -> list[dict[str, str]]:
    return list(KNOT_TABLE)


def get_knot(name: str) -> dict[str, str] | None:
    for k in KNOT_TABLE:
        if k["name"] == name:
            return k
    return None


def jones_polynomial_trefoil() -> sp.Expr:
    """Jones polynomial of the trefoil knot."""
    q = sp.Symbol("q")
    return -q ** (-4) - q ** (-3) + q ** (-1)


def alexander_polynomial_trefoil() -> sp.Expr:
    """Alexander polynomial of the trefoil knot."""
    t = sp.Symbol("t")
    return t ** 2 - t + 1


def jones_polynomial_unknot() -> int:
    return 1


def linking_number(crossings: list[tuple[int, int, int]]) -> int:
    """Compute the linking number from a list of signed crossings.

    crossings: list of (component_a, component_b, sign)
    """
    return sum(c[2] for c in crossings) // 2


def is_unknot(jones: sp.Expr) -> bool:
    return sp.simplify(jones - 1) == 0


__all__ = [
    "KNOT_TABLE", "list_knots", "get_knot", "jones_polynomial_trefoil",
    "alexander_polynomial_trefoil", "jones_polynomial_unknot", "linking_number", "is_unknot",
]
