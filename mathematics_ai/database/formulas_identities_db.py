"""Mathematical identities, integrals and special functions."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).resolve().parent / "formulas_identities.json"

_DEFAULT_FORMULAS: list[dict[str, str]] = [
    {"name": "Euler's identity", "formula": "e^(i*pi) + 1 = 0", "field": "analysis"},
    {"name": "Binomial theorem", "formula": "(x+y)^n = sum C(n,k) x^k y^(n-k)", "field": "algebra"},
    {"name": "Sum of first n integers", "formula": "sum_{k=1}^n k = n(n+1)/2", "field": "combinatorics"},
    {"name": "Sum of squares", "formula": "sum_{k=1}^n k^2 = n(n+1)(2n+1)/6", "field": "combinatorics"},
    {"name": "Sum of cubes", "formula": "sum_{k=1}^n k^3 = (n(n+1)/2)^2", "field": "combinatorics"},
    {"name": "Gaussian integral", "formula": "integral e^(-x^2) dx = sqrt(pi)", "field": "analysis"},
    {"name": "Stirling's approximation", "formula": "n! ~ sqrt(2*pi*n) (n/e)^n", "field": "analysis"},
    {"name": "Gamma function", "formula": "Gamma(n+1) = n!", "field": "analysis"},
    {"name": "Wallis product", "formula": "pi/2 = prod (4n^2)/(4n^2-1)", "field": "analysis"},
    {"name": "Cauchy integral formula", "formula": "f(a) = 1/(2*pi*i) oint f(z)/(z-a) dz", "field": "complex_analysis"},
    {"name": "Residue theorem", "formula": "oint f(z) dz = 2*pi*i * sum Res(f, a_k)", "field": "complex_analysis"},
    {"name": "Jensen's inequality", "formula": "E[f(X)] >= f(E[X]) for convex f", "field": "probability"},
]


def _load() -> list[dict[str, str]]:
    if not DB_FILE.exists():
        _save(_DEFAULT_FORMULAS)
    with open(DB_FILE) as f:
        return json.load(f)


def _save(data: list[dict[str, str]]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def search(query: str) -> list[dict[str, str]]:
    data = _load()
    q = query.lower()
    return [f for f in data if q in f["name"].lower() or q in f["formula"].lower() or q in f["field"].lower()]


def get(name: str) -> dict[str, str] | None:
    for f in _load():
        if f["name"].lower() == name.lower():
            return f
    return None


def list_all() -> list[dict[str, str]]:
    return _load()


def add(formula: dict[str, str]) -> None:
    data = _load()
    data.append(formula)
    _save(data)


__all__ = ["search", "get", "list_all", "add", "DB_FILE"]
