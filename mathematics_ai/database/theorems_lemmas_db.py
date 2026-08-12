"""Database of known mathematical theorems and proofs.

Uses a JSON-backed store (no external DB needed). The schema mirrors what a
real SQLite database would contain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).resolve().parent / "theorems_lemmas.json"

_DEFAULT_THEOREMS: list[dict[str, str]] = [
    {"name": "Pythagorean Theorem", "statement": "a^2 + b^2 = c^2", "field": "geometry", "proof": "Euclidean dissection"},
    {"name": "Fundamental Theorem of Arithmetic", "statement": "Every integer > 1 has a unique prime factorization", "field": "number_theory", "proof": "by strong induction"},
    {"name": "Fundamental Theorem of Calculus", "statement": "integral of f = F(b) - F(a) where F' = f", "field": "analysis", "proof": "mean value theorem"},
    {"name": "Fundamental Theorem of Algebra", "statement": "Every non-constant polynomial has a complex root", "field": "algebra", "proof": "Liouville's theorem"},
    {"name": "Euler's Formula", "statement": "e^(i*x) = cos(x) + i*sin(x)", "field": "analysis", "proof": "Taylor series"},
    {"name": "Cauchy-Schwarz Inequality", "statement": "|<u,v>| <= ||u|| ||v||", "field": "linear_algebra", "proof": "discriminant of a quadratic"},
    {"name": "AM-GM Inequality", "statement": "(a+b)/2 >= sqrt(a*b)", "field": "analysis", "proof": "by square expansion"},
    {"name": "Lagrange's Theorem", "statement": "|H| divides |G| for subgroup H of finite group G", "field": "algebra", "proof": "cosets partition G"},
    {"name": "Euler's Totient Theorem", "statement": "a^phi(n) = 1 mod n if gcd(a,n)=1", "field": "number_theory", "proof": "group of units"},
    {"name": "Gauss's Lemma", "statement": "product of two primitive polynomials is primitive", "field": "algebra", "proof": "contradiction on prime divisors"},
]


def _load() -> list[dict[str, str]]:
    if not DB_FILE.exists():
        _save(_DEFAULT_THEOREMS)
    with open(DB_FILE) as f:
        return json.load(f)


def _save(data: list[dict[str, str]]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def search(query: str) -> list[dict[str, str]]:
    data = _load()
    q = query.lower()
    return [t for t in data if q in t["name"].lower() or q in t["statement"].lower() or q in t["field"].lower()]


def get(name: str) -> dict[str, str] | None:
    for t in _load():
        if t["name"].lower() == name.lower():
            return t
    return None


def list_all() -> list[dict[str, str]]:
    return _load()


def add(theorem: dict[str, str]) -> None:
    data = _load()
    data.append(theorem)
    _save(data)


__all__ = ["search", "get", "list_all", "add", "DB_FILE"]
