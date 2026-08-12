"""Classify manifolds, orbifolds and symmetry groups."""

from __future__ import annotations

from typing import Any

import sympy as sp


MANIFOLD_CLASSES: dict[str, dict[str, Any]] = {
    "R": {"dimension": 1, "type": "smooth", "curvature": 0, "orientable": True},
    "S1": {"dimension": 1, "type": "smooth", "curvature": 0, "orientable": True},
    "S2": {"dimension": 2, "type": "smooth", "curvature": 1, "orientable": True, "euler": 2},
    "T2": {"dimension": 2, "type": "smooth", "curvature": 0, "orientable": True, "euler": 0},
    "RP2": {"dimension": 2, "type": "smooth", "curvature": 1, "orientable": False, "euler": 1},
    "RP3": {"dimension": 3, "type": "smooth", "curvature": 0, "orientable": True, "euler": 0},
    "S3": {"dimension": 3, "type": "smooth", "curvature": 1, "orientable": True, "euler": 0},
    "Klein_bottle": {"dimension": 2, "type": "smooth", "curvature": 0, "orientable": False, "euler": 0},
    "Torus_Tn": {"dimension": "n", "type": "smooth", "curvature": 0, "orientable": True, "euler": 0},
}


def classify_manifold(properties: dict[str, Any]) -> list[str]:
    """Given properties (dimension, orientable, euler, curvature), suggest candidates."""
    candidates = []
    for name, props in MANIFOLD_CLASSES.items():
        match = True
        for key, val in properties.items():
            if key in props and props[key] != val:
                match = False
                break
        if match:
            candidates.append(name)
    return candidates


def get_manifold(name: str) -> dict[str, Any] | None:
    return MANIFOLD_CLASSES.get(name)


def classify_by_euler(euler: int, dim: int, orientable: bool = True) -> list[str]:
    props = {"dimension": dim, "orientable": orientable, "euler": euler}
    return classify_manifold(props)


def classify_finite_group(elements: list[Any], multiplication_table: list[list[int]]) -> dict[str, Any]:
    """Classify a finite group given its multiplication table."""
    n = len(elements)
    is_abelian = all(multiplication_table[i][j] == multiplication_table[j][i] for i in range(n) for j in range(n))
    # find identity
    identity = None
    for i in range(n):
        if all(multiplication_table[i][j] == j and multiplication_table[j][i] == j for j in range(n)):
            identity = i
            break
    return {
        "order": n,
        "abelian": is_abelian,
        "identity_index": identity,
        "cyclic": is_abelian and _is_cyclic(multiplication_table, identity),
    }


def _is_cyclic(table: list[list[int]], identity: int | None) -> bool:
    n = len(table)
    if identity is None:
        return False
    for g in range(n):
        powers = [g]
        current = g
        for _ in range(n):
            current = table[current][g]
            if current == identity and len(set(powers)) == n - 1 and identity not in powers:
                return True
            powers.append(current)
            if current == g:
                break
    return False


def classify_orbifold(signature: str) -> dict[str, Any]:
    """Orbifold signature -> Euler characteristic (2D)."""
    # e.g. "2.2" for a football, "*" for disc
    s = signature.replace("*", "")
    parts = s.split(".")
    euler = 2
    for p in parts:
        if p:
            try:
                euler -= 1.0 / int(p)
            except ValueError:
                pass
    return {"signature": signature, "euler_characteristic": euler}


__all__ = [
    "MANIFOLD_CLASSES", "classify_manifold", "get_manifold",
    "classify_by_euler", "classify_finite_group", "classify_orbifold",
]
