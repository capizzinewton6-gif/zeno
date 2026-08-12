"""Network, DAG and graph theory layout engines."""

from __future__ import annotations

from typing import Any

import numpy as np


def spring_layout(adjacency: list[list[int]], iterations: int = 50, seed: int = 42) -> list[tuple[float, float]]:
    """Fruchterman-Reingold-style spring layout."""
    n = len(adjacency)
    A = np.array(adjacency, dtype=float)
    rng = np.random.default_rng(seed)
    pos = rng.uniform(-1, 1, (n, 2))
    k = 1.0 / np.sqrt(n)
    for _ in range(iterations):
        disp = np.zeros((n, 2))
        for i in range(n):
            for j in range(n):
                if i != j:
                    delta = pos[i] - pos[j]
                    dist = np.linalg.norm(delta) + 1e-9
                    disp[i] += (delta / dist) * (k * k) / dist
        for i in range(n):
            for j in range(n):
                if A[i, j] > 0:
                    delta = pos[j] - pos[i]
                    dist = np.linalg.norm(delta) + 1e-9
                    disp[i] += (delta / dist) * (dist * dist) / k
        for i in range(n):
            pos[i] += disp[i] / (np.linalg.norm(disp[i]) + 1e-9) * min(np.linalg.norm(disp[i]), 0.1)
    # normalize to [0, 1]
    pos = (pos - pos.min(axis=0)) / (pos.max(axis=0) - pos.min(axis=0) + 1e-9)
    return [tuple(p) for p in pos]


def topological_sort(adjacency: list[list[int]]) -> list[int] | None:
    """Kahn's algorithm; returns None if cycle detected."""
    n = len(adjacency)
    in_degree = [sum(adjacency[i][j] for i in range(n)) for j in range(n)]  # note: depends on direction
    # Recompute: assume adjacency[i][j] = 1 means edge i->j
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adjacency[i][j]:
                in_degree[j] += 1
    queue = [i for i in range(n) if in_degree[i] == 0]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for j in range(n):
            if adjacency[node][j]:
                in_degree[j] -= 1
                if in_degree[j] == 0:
                    queue.append(j)
    return order if len(order) == n else None


def spectral_layout(adjacency: list[list[int]]) -> list[tuple[float, float]]:
    """Eigenvector-based layout using the graph Laplacian."""
    A = np.array(adjacency, dtype=float)
    D = np.diag(A.sum(axis=1))
    L = D - A
    eigvals, eigvecs = np.linalg.eigh(L)
    # use 2nd and 3rd smallest eigenvectors
    coords = eigvecs[:, 1:3]
    coords = (coords - coords.min(axis=0)) / (coords.max(axis=0) - coords.min(axis=0) + 1e-9)
    return [tuple(c) for c in coords]


__all__ = ["spring_layout", "topological_sort", "spectral_layout"]
