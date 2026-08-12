"""Vector spaces, operator theory and matrix algebra.

Backed by SymPy for exact symbolic linear algebra.
"""

from __future__ import annotations

from typing import Any

import sympy as sp
import numpy as np


def matrix(rows: list[list[Any]]) -> sp.Matrix:
    return sp.Matrix(rows)


def eigen(matrix: Any) -> dict[str, list[Any]]:
    M = sp.Matrix(matrix)
    eig = M.eigenvects()
    return {
        "eigenvalues": [val for val, _, _ in eig],
        "eigenvectors": [[vec.tolist() for vec in vecs] for _, _, vecs in eig],
    }


def determinant(matrix: Any) -> Any:
    return sp.Matrix(matrix).det()


def inverse(matrix: Any) -> sp.Matrix:
    return sp.Matrix(matrix).inv()


def rank(matrix: Any) -> int:
    return sp.Matrix(matrix).rank()


def nullity(matrix: Any) -> int:
    return sp.Matrix(matrix).cols - sp.Matrix(matrix).rank()


def svd_numpy(matrix: Any) -> dict[str, Any]:
    """Singular Value Decomposition via NumPy (numeric)."""
    U, S, Vt = np.linalg.svd(np.array(matrix, dtype=float))
    return {"U": U.tolist(), "singular_values": S.tolist(), "Vt": Vt.tolist()}


def qr_decomposition(matrix: Any) -> dict[str, Any]:
    Q, R = sp.Matrix(matrix).QRdecomposition()
    return {"Q": Q.tolist(), "R": R.tolist()}


def solve_linear_system(A: Any, b: Any) -> Any:
    """Solve Ax = b. Returns the solution or None if singular."""
    M = sp.Matrix(A)
    bb = sp.Matrix(b)
    try:
        return M.solve(bb)
    except Exception:
        return None


def lu_decomposition(matrix: Any) -> dict[str, Any]:
    L, U, _ = sp.Matrix(matrix).LUdecomposition()
    return {"L": L.tolist(), "U": U.tolist()}


def is_orthogonal(matrix: Any) -> bool:
    M = sp.Matrix(matrix)
    return sp.simplify(M.T * M - sp.eye(M.cols)) == sp.zeros(M.rows, M.cols)


def is_symmetric(matrix: Any) -> bool:
    M = sp.Matrix(matrix)
    return M.equals(M.T)


def diagonalize(matrix: Any) -> dict[str, Any]:
    M = sp.Matrix(matrix)
    P, D = M.diagonalize()
    return {"P": P.tolist(), "D": D.tolist()}


def gram_schmidt(vectors: list[list[Any]]) -> list[list[Any]]:
    """Orthonormalize a set of vectors via Gram-Schmidt."""
    basis = []
    for v in vectors:
        w = sp.Matrix(v)
        for b in basis:
            w -= (w.dot(b) / b.dot(b)) * b
        if w.norm() != 0:
            basis.append(w / w.norm())
    return [b.tolist() for b in basis]


__all__ = [
    "matrix", "eigen", "determinant", "inverse", "rank", "nullity",
    "svd_numpy", "qr_decomposition", "solve_linear_system", "lu_decomposition",
    "is_orthogonal", "is_symmetric", "diagonalize", "gram_schmidt",
]
