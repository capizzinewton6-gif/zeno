"""Identify handwritten mathematical notation and Greek symbols."""

from __future__ import annotations

from typing import Any

GREEK_SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "iota": "ι", "kappa": "κ",
    "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π",
    "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ",
    "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ",
    "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}

MATH_OPERATORS = {
    "sum": "∑", "prod": "∏", "int": "∫", "oint": "∮",
    "partial": "∂", "nabla": "∇", "infty": "∞", "sqrt": "√",
    "approx": "≈", "neq": "≠", "leq": "≤", "geq": "≥",
    "pm": "±", "times": "×", "div": "÷", "cdot": "·",
    "in": "∈", "notin": "∉", "subset": "⊂", "supset": "⊃",
    "cap": "∩", "cup": "∪", "forall": "∀", "exists": "∃",
    "rightarrow": "→", "leftarrow": "←", "leftrightarrow": "↔",
    "Rightarrow": "⇒", "Leftarrow": "⇐", "Leftrightarrow": "⇔",
}


def name_to_symbol(name: str) -> str | None:
    if name in GREEK_SYMBOLS:
        return GREEK_SYMBOLS[name]
    if name in MATH_OPERATORS:
        return MATH_OPERATORS[name]
    return None


def symbol_to_name(symbol: str) -> str | None:
    for d in (GREEK_SYMBOLS, MATH_OPERATORS):
        for k, v in d.items():
            if v == symbol:
                return k
    return None


def identify_from_text(text: str) -> list[dict[str, str]]:
    """Identify Greek letters / operators mentioned by name in text."""
    found = []
    words = text.replace("\\", " ").split()
    for w in words:
        sym = name_to_symbol(w)
        if sym:
            found.append({"name": w, "symbol": sym})
    return found


__all__ = ["GREEK_SYMBOLS", "MATH_OPERATORS", "name_to_symbol", "symbol_to_name", "identify_from_text"]
