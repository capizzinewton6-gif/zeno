"""Lie algebra structure constants, root systems and representations."""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp


# Cartan matrix for each simple Lie algebra type (small ranks).
CARTAN_MATRICES: dict[str, list[list[int]]] = {
    "A1": [[2]],
    "A2": [[2, -1], [-1, 2]],
    "A3": [[2, -1, 0], [-1, 2, -1], [0, -1, 2]],
    "B2": [[2, -2], [-1, 2]],
    "G2": [[2, -1], [-3, 2]],
}


def get_cartan_matrix(algebra: str) -> list[list[int]] | None:
    return CARTAN_MATRICES.get(algebra)


def dimension_of_algebra(algebra: str) -> int | None:
    """Dimension of the simple Lie algebra = rank + #roots."""
    C = get_cartan_matrix(algebra)
    if C is None:
        return None
    rank = len(C)
    n_positive = 0
    # count positive roots (simplified)
    n_positive = rank * (rank + 1) // 2 if algebra.startswith("A") else rank * (rank + 1)
    return rank + 2 * n_positive


def structure_constants_su2() -> dict[tuple[int, int], int]:
    """[T_a, T_b] = i * epsilon_{abc} T_c for su(2)."""
    return {(1, 2): 3, (2, 3): 1, (3, 1): 2}


def root_system_A2() -> list[list[float]]:
    """Root system of A2 (hexagon)."""
    return [
        [1, 0], [-1, 0],
        [0.5, np.sqrt(3) / 2], [-0.5, -np.sqrt(3) / 2],
        [0.5, -np.sqrt(3) / 2], [-0.5, np.sqrt(3) / 2],
    ]


def weyl_group_orbit(root: list[float], cartan: list[list[int]]) -> list[list[float]]:
    """Compute the orbit of a root under the Weyl group (simplified)."""
    v = np.array(root, dtype=float)
    orbit = [v.tolist()]
    for _ in range(len(cartan) ** 2):
        for i in range(len(cartan)):
            v = v - 2 * np.dot(v, cartan[i]) / np.dot(cartan[i], cartan[i]) * np.array(cartan[i])
            if not any(np.allclose(v, o) for o in orbit):
                orbit.append(v.tolist())
    return orbit


def fundamental_representation_dim(algebra: str) -> int:
    """Dimension of the fundamental representation."""
    if algebra == "A1":
        return 2
    if algebra == "A2":
        return 3
    if algebra == "B2":
        return 4
    if algebra == "G2":
        return 7
    return 0


__all__ = [
    "CARTAN_MATRICES", "get_cartan_matrix", "dimension_of_algebra",
    "structure_constants_su2", "root_system_A2", "weyl_group_orbit",
    "fundamental_representation_dim",
]
