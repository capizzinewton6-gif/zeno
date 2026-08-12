"""Automated tactic generation (simp, auto, ring, omega, ...)."""

from __future__ import annotations

from typing import Any


TACTIC_LIBRARY: dict[str, str] = {
    "algebraic_identity": "ring",
    "linear_arithmetic": "linarith",
    "nonlinear_arithmetic": "nlinarith",
    "natural_number_arithmetic": "omega",
    "simplification": "simp",
    "induction": "induction n with",
    "rewrite": "rw [",
    "exact": "exact",
    "decidable": "decide",
    "tautology": "tauto",
    "contradiction": "contradiction",
    "norm_num": "norm_num",
}


def suggest_tactic(goal: str, context: str = "") -> str:
    """Suggest a tactic for a proof goal based on keywords."""
    g = goal.lower()
    if any(k in g for k in ("for all", "for every", "induct")):
        return TACTIC_LIBRARY["induction"]
    if any(k in g for k in ("<", ">", "≤", "≥", "inequality")):
        return TACTIC_LIBRARY["linear_arithmetic"]
    if "sum" in g or "Σ" in g:
        return TACTIC_LIBRARY["nonlinear_arithmetic"]
    if any(k in g for k in ("even", "odd", "mod", "divisible")):
        return TACTIC_LIBRARY["natural_number_arithmetic"]
    if "=" in g and "<" not in g and ">" not in g:
        if any(c in g for c in "+-*/^"):
            return TACTIC_LIBRARY["algebraic_identity"]
        return TACTIC_LIBRARY["simplification"]
    return TACTIC_LIBRARY["simplification"]


def generate_tactic_sequence(goal: str) -> list[str]:
    """Generate a plausible tactic sequence for a goal."""
    primary = suggest_tactic(goal)
    return [primary, "exact rfl"] if primary != "induction n with" else [primary + " | zero | succ", "simp"]


__all__ = ["TACTIC_LIBRARY", "suggest_tactic", "generate_tactic_sequence"]
