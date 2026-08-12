"""Mathematical logic, set theory and model theory helpers."""

from __future__ import annotations

from typing import Any

import sympy as sp
from sympy.logic.boolalg import And, Or, Not, Implies, Xor, to_cnf, to_dnf, simplify_logic
from sympy.logic import satisfiable


def parse_proposition(expr: str) -> sp.Expr:
    """Parse a propositional formula string into a SymPy boolean expression."""
    return sp.sympify(expr, locals={"implies": Implies, "xor": Xor})


def to_cnf_form(expr: Any) -> sp.Expr:
    return to_cnf(sp.sympify(expr))


def to_dnf_form(expr: Any) -> sp.Expr:
    return to_dnf(sp.sympify(expr))


def is_satisfiable(expr: Any) -> bool:
    return bool(satisfiable(sp.sympify(expr)))


def is_tautology(expr: Any) -> bool:
    e = sp.sympify(expr)
    return not satisfiable(Not(e))


def is_contradiction(expr: Any) -> bool:
    return not satisfiable(sp.sympify(expr))


def simplify_logical(expr: Any) -> sp.Expr:
    return simplify_logic(sp.sympify(expr))


def truth_table(expr: Any, symbols: list[sp.Symbol]) -> list[dict[str, bool | Any]]:
    """Full truth table for ``expr`` over the given boolean symbols."""
    e = sp.sympify(expr)
    rows = []
    n = len(symbols)
    for bits in range(2 ** n):
        assignment = {symbols[i]: bool((bits >> i) & 1) for i in range(n)}
        val = bool(e.subs(assignment))
        rows.append({**{str(s): v for s, v in assignment.items()}, "result": val})
    return rows


def set_operations(a: set[Any], b: set[Any]) -> dict[str, set[Any]]:
    return {
        "union": a | b,
        "intersection": a & b,
        "difference": a - b,
        "symmetric_difference": a ^ b,
    }


__all__ = [
    "parse_proposition", "to_cnf_form", "to_dnf_form", "is_satisfiable",
    "is_tautology", "is_contradiction", "simplify_logical", "truth_table",
    "set_operations",
]
