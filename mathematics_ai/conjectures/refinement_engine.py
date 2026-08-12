"""Refine and generalize mathematical theorems."""

from __future__ import annotations

from typing import Any


def refine_statement(statement: str, conditions: list[str]) -> str:
    """Add explicit hypotheses to a theorem statement."""
    if not conditions:
        return statement
    prefix = "Under the assumptions: " + "; ".join(conditions) + ". "
    return prefix + statement


def generalize(pattern: dict[str, Any], dimension: int = 1) -> dict[str, Any]:
    """Suggest a generalization of an identified pattern."""
    t = pattern.get("type")
    if t == "arithmetic":
        return {"generalization": "linear sequence a_n = a_0 + n*d", "dimensions": dimension}
    if t == "geometric":
        return {"generalization": "exponential sequence a_n = a_0 * r^n", "dimensions": dimension}
    if t == "quadratic":
        return {"generalization": "polynomial sequence of degree 2", "dimensions": dimension}
    if t == "fibonacci":
        return {"generalization": "linear recurrence a_n = a_(n-1) + a_(n-2); possibly a_n = p*a_(n-1) + q*a_(n-2)", "dimensions": dimension}
    return {"generalization": "no obvious generalization", "dimensions": dimension}


def weaken_conclusion(statement: str) -> str:
    """Produce a weaker version of a theorem (easier to prove fallback)."""
    return f"Weak form: {statement} holds for sufficiently large n."


__all__ = ["refine_statement", "generalize", "weaken_conclusion"]
