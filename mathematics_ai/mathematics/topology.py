"""Point-set, algebraic and differential topology helpers.

Uses simplicial complexes (via NetworkX) and basic homotopy invariants.
"""

from __future__ import annotations

from typing import Iterable

import networkx as nx
import numpy as np


class SimplicialComplex:
    """A finite simplicial complex stored as a list of simplices (tuples)."""

    def __init__(self, simplices: Iterable[tuple[int, ...]]) -> None:
        # Closure: include all faces of every simplex.
        closed: set[tuple[int, ...]] = set()
        for simplex in simplices:
            simplex = tuple(sorted(simplex))
            closed.add(simplex)
            # all faces
            n = len(simplex)
            from itertools import combinations
            for r in range(n):
                for face in combinations(simplex, r):
                    closed.add(tuple(sorted(face)))
        self.simplices = closed

    def faces(self, dim: int) -> list[tuple[int, ...]]:
        return [s for s in self.simplices if len(s) == dim + 1]

    def euler_characteristic(self) -> int:
        chi = 0
        for s in self.simplices:
            dim = len(s) - 1
            if dim >= 0:
                chi += (-1) ** dim
        return chi

    def f_vector(self) -> list[int]:
        if not self.simplices:
            return []
        max_dim = max(len(s) - 1 for s in self.simplices)
        return [len([s for s in self.simplices if len(s) - 1 == d]) for d in range(max_dim + 1)]

    def boundary_matrix(self, dim: int) -> np.ndarray:
        """Integer boundary matrix ∂_dim : C_dim -> C_{dim-1}."""
        cols = self.faces(dim)
        rows = self.faces(dim - 1) if dim > 0 else []
        if not cols:
            return np.zeros((len(rows), 0), dtype=int)
        row_index = {f: i for i, f in enumerate(rows)}
        B = np.zeros((len(rows), len(cols)), dtype=int)
        for j, simplex in enumerate(cols):
            from itertools import combinations
            for k, face in enumerate(combinations(simplex, len(simplex) - 1)):
                face = tuple(sorted(face))
                # face for a 0-simplex is the empty tuple; skip (no C_{-1}).
                if face not in row_index:
                    continue
                i = row_index[face]
                B[i, j] += (-1) ** k
        return B

    def betti_numbers(self, max_dim: int = 2) -> list[int]:
        """Compute Betti numbers via Smith normal form of boundary matrices."""
        def smith_rank(M: np.ndarray) -> int:
            """Integer rank via fraction-free Gaussian elimination."""
            if M.size == 0:
                return 0
            M = M.astype(int).copy()
            rows, cols = M.shape
            rank = 0
            for col in range(cols):
                # find a non-zero pivot at or below `rank`
                pivot = None
                for r in range(rank, rows):
                    if M[r, col] != 0:
                        pivot = r
                        break
                if pivot is None:
                    continue
                M[[rank, pivot]] = M[[pivot, rank]]
                # eliminate this column from all other rows
                for r in range(rows):
                    if r != rank and M[r, col] != 0:
                        # row[r] = a*row[r] - b*row[rank] with a=M[rank,col], b=M[r,col]
                        a, b = int(M[rank, col]), int(M[r, col])
                        M[r] = a * M[r] - b * M[rank]
                rank += 1
                if rank == rows:
                    break
            return rank
        betti = []
        for d in range(max_dim + 1):
            rank_d = smith_rank(self.boundary_matrix(d))
            rank_d1 = smith_rank(self.boundary_matrix(d + 1))
            n_d = len(self.faces(d))
            betti.append(n_d - rank_d - rank_d1)
        return betti


def graph_to_complex(edges: Iterable[tuple[int, int]]) -> SimplicialComplex:
    simplices = [(u, v) for u, v in edges] + [(i,) for u, v in edges for i in (u, v)]
    return SimplicialComplex(simplices)


def connected_components(graph: nx.Graph) -> int:
    return nx.number_connected_components(graph)


__all__ = ["SimplicialComplex", "graph_to_complex", "connected_components"]
