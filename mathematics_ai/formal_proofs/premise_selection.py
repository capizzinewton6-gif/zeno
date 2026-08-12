"""Retrieve relevant lemmas and axioms from formal libraries.

In this environment Mathlib is not indexed, so this module uses a small
built-in catalogue of well-known theorems and matches by keyword. The interface
mirrors what a real Mathlib index would provide.
"""

from __future__ import annotations

from typing import Any

LEMMA_CATALOG: list[dict[str, str]] = [
    {"name": "add_comm", "statement": "a + b = b + a", "tags": "algebra arithmetic commutativity"},
    {"name": "add_assoc", "statement": "(a + b) + c = a + (b + c)", "tags": "algebra arithmetic associativity"},
    {"name": "mul_comm", "statement": "a * b = b * a", "tags": "algebra arithmetic commutativity"},
    {"name": "mul_assoc", "statement": "(a * b) * c = a * (b * c)", "tags": "algebra arithmetic associativity"},
    {"name": "pythagoras", "statement": "sin(x)^2 + cos(x)^2 = 1", "tags": "trigonometry identity"},
    {"name": "even_iff", "statement": "even n <-> n mod 2 = 0", "tags": "number theory parity"},
    {"name": "fermat_little", "statement": "p prime -> a^(p-1) = 1 mod p", "tags": "number theory primes modular"},
    {"name": "cauchy_schwarz", "statement": "|<u,v>| <= ||u|| * ||v||", "tags": "linear algebra inequality inner product"},
    {"name": "am_gm", "statement": "(a + b) / 2 >= sqrt(a * b)", "tags": "inequality means"},
    {"name": "binomial_theorem", "statement": "(x + y)^n = sum binomial(n,k) x^k y^(n-k)", "tags": "algebra combinatorics"},
    {"name": "fubini", "statement": "integral f = integral (integral f)", "tags": "analysis integration measure"},
    {"name": "stokes", "statement": "integral boundary omega = integral manifold d(omega)", "tags": "geometry topology differential"},
]


def retrieve(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Retrieve lemmas matching the query by keyword overlap."""
    q = query.lower()
    scored = []
    for lemma in LEMMA_CATALOG:
        score = sum(q.count(t) for t in lemma["tags"].split())
        score += 2 if lemma["name"].lower() in q else 0
        if score > 0:
            scored.append((score, lemma))
    scored.sort(key=lambda x: -x[0])
    return [l for _, l in scored[:max_results]]


def list_all() -> list[dict[str, str]]:
    return list(LEMMA_CATALOG)


__all__ = ["retrieve", "list_all", "LEMMA_CATALOG"]
