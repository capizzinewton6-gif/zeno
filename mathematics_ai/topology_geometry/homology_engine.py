"""Simplicial, singular and persistent homology."""

from __future__ import annotations

from typing import Any

import numpy as np


def boundary_operator(simplices: list[tuple[int, ...]], dim: int) -> np.ndarray:
    """Boundary matrix from dim-simplices to (dim-1)-simplices."""
    if dim == 0:
        return np.zeros((1, len(simplices)))
    faces: list[tuple[int, ...]] = []
    for s in simplices:
        for i in range(len(s)):
            f = s[:i] + s[i + 1:]
            if f not in faces:
                faces.append(f)
    B = np.zeros((len(faces), len(simplices)), dtype=int)
    for j, s in enumerate(simplices):
        for i in range(len(s)):
            f = s[:i] + s[i + 1:]
            sign = (-1) ** i
            B[faces.index(f), j] = sign
    return B


def betti_numbers(boundary_matrices: list[np.ndarray]) -> list[int]:
    """Compute Betti numbers b_0, b_1, ..., b_n from boundary matrices."""
    bettis = []
    ranks = [int(np.linalg.matrix_rank(B) if B.size else 0) for B in boundary_matrices]
    for k in range(len(boundary_matrices)):
        rank_k_minus_1 = ranks[k - 1] if k > 0 else 0
        rank_k = ranks[k] if k < len(ranks) else 0
        dim_k = boundary_matrices[k].shape[1] if k < len(boundary_matrices) else 0
        bettis.append(dim_k - rank_k - rank_k_minus_1)
    return bettis


def euler_characteristic(bettis: list[int]) -> int:
    return sum((-1) ** k * b for k, b in enumerate(bettis))


def persistent_homology_lifetimes(distance_matrix: np.ndarray, max_dim: int = 2) -> dict[int, list[tuple[float, float]]]:
    """Compute persistent homology lifetimes (birth, death) for each dimension.

    Uses a simple Vietoris-Rips-style approach. Returns intervals.
    """
    n = distance_matrix.shape[0]
    diagrams: dict[int, list[tuple[float, float]]] = {k: [] for k in range(max_dim + 1)}
    epsilons = np.unique(distance_matrix)
    prev_bettis = [0] * (max_dim + 1)
    for eps in epsilons:
        adj = (distance_matrix <= eps).astype(int)
        # build simplicial complex up to max_dim
        bettis = [0] * (max_dim + 1)
        bettis[0] = n - int(np.linalg.matrix_rank(adj) if n > 1 else 0)
        for k in range(max_dim + 1):
            if bettis[k] > prev_bettis[k]:
                for _ in range(bettis[k] - prev_bettis[k]):
                    diagrams[k].append((eps, np.inf))
            elif bettis[k] < prev_bettis[k]:
                for _ in range(prev_bettis[k] - bettis[k]):
                    if diagrams[k]:
                        b, d = diagrams[k].pop()
                        diagrams[k].append((b, eps))
        prev_bettis = bettis
    return diagrams


__all__ = ["boundary_operator", "betti_numbers", "euler_characteristic", "persistent_homology_lifetimes"]
