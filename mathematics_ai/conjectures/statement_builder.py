"""Formalize mathematical propositions from patterns."""

from __future__ import annotations

from typing import Any


def build_conjecture(name: str, sequence: list[int | float], pattern: dict[str, Any], polynomial: Any = None) -> str:
    """Produce a natural-language conjecture statement from a pattern."""
    ptype = pattern.get("type", "unknown")
    sample = sequence[:5]
    if ptype == "arithmetic":
        d = pattern.get("common_difference")
        return f"Conjecture ({name}): the sequence {sample}... is arithmetic with common difference {d}."
    if ptype == "geometric":
        r = pattern.get("common_ratio")
        return f"Conjecture ({name}): the sequence {sample}... is geometric with common ratio {r}."
    if ptype == "quadratic":
        sd = pattern.get("second_difference")
        return f"Conjecture ({name}): the sequence {sample}... is quadratic with constant second difference {sd}."
    if ptype == "fibonacci":
        return f"Conjecture ({name}): the sequence {sample}... satisfies the Fibonacci recurrence a_n = a_(n-1) + a_(n-2)."
    if polynomial is not None:
        return f"Conjecture ({name}): a_n = {polynomial} for n = 0,1,2,..."
    return f"Conjecture ({name}): the sequence {sample}... follows an unidentified pattern."


def to_formal(statement: str) -> str:
    """Light markup for formal rendering (placeholder for Lean/Coq output)."""
    return f"/* formal conjecture */\n-- {statement}"


__all__ = ["build_conjecture", "to_formal"]
