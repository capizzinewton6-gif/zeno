"""Axiom systems: ZFC, Peano, Category axioms, Non-Euclidean."""

from __future__ import annotations

from typing import Any

AXIOM_SYSTEMS: dict[str, list[str]] = {
    "ZFC": [
        "Axiom of Extensionality",
        "Axiom of Regularity",
        "Axiom Schema of Specification",
        "Axiom of Pairing",
        "Axiom of Union",
        "Axiom Schema of Replacement",
        "Axiom of Infinity",
        "Axiom of Power Set",
        "Axiom of Well-Ordering (Choice)",
    ],
    "Peano": [
        "0 is a natural number",
        "Every natural number n has a successor S(n)",
        "0 is not the successor of any natural number",
        "S is injective",
        "Axiom of Induction",
    ],
    "Category": [
        "For every object there exists an identity morphism",
        "Morphisms compose associatively",
        "Identities act as units under composition",
    ],
    "Non-Euclidean_Hyperbolic": [
        "Through a point not on a line, infinitely many parallel lines exist (negation of the parallel postulate)",
        "The angle sum of a triangle is less than 180°",
    ],
    "Non-Euclidean_Elliptic": [
        "No parallel lines exist (all lines intersect)",
        "The angle sum of a triangle is greater than 180°",
    ],
    "Group": [
        "Closure under the binary operation",
        "Associativity",
        "Existence of an identity element",
        "Existence of inverses",
    ],
    "Field": [
        "Additive group axioms",
        "Multiplicative group axioms (excluding 0)",
        "Distributivity of multiplication over addition",
    ],
}


def get_axioms(system: str) -> list[str]:
    return AXIOM_SYSTEMS.get(system, [])


def list_systems() -> list[str]:
    return list(AXIOM_SYSTEMS.keys())


def check_independence(axioms: list[str], theorem: str) -> dict[str, Any]:
    """Heuristic: returns whether the theorem is provable from the axioms.

    Real independence checking requires a proof assistant; this is a placeholder.
    """
    return {
        "axioms": axioms,
        "theorem": theorem,
        "independent": False,
        "note": "independence checking requires a formal proof assistant",
    }


__all__ = ["AXIOM_SYSTEMS", "get_axioms", "list_systems", "check_independence"]
