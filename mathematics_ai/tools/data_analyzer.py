"""Analyze numerical matrices and algebraic structures."""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp


def matrix_summary(matrix: list[list[float]]) -> dict[str, Any]:
    """Summary statistics of a numeric matrix."""
    A = np.array(matrix, dtype=float)
    return {
        "shape": list(A.shape),
        "rank": int(np.linalg.matrix_rank(A)),
        "determinant": float(np.linalg.det(A)) if A.shape[0] == A.shape[1] else None,
        "trace": float(np.trace(A)) if A.shape[0] == A.shape[1] else None,
        "frobenius_norm": float(np.linalg.norm(A)),
        "min": float(A.min()),
        "max": float(A.max()),
        "mean": float(A.mean()),
        "std": float(A.std()),
        "condition_number": float(np.linalg.cond(A)) if A.shape[0] == A.shape[1] else None,
    }


def is_symmetric(matrix: list[list[float]], tol: float = 1e-9) -> bool:
    A = np.array(matrix, dtype=float)
    return A.shape[0] == A.shape[1] and np.allclose(A, A.T, atol=tol)


def is_positive_definite(matrix: list[list[float]]) -> bool:
    try:
        np.linalg.cholesky(np.array(matrix, dtype=float))
        return True
    except np.linalg.LinAlgError:
        return False


def is_stochastic(matrix: list[list[float]], tol: float = 1e-9) -> bool:
    """Check if a matrix is (row) stochastic."""
    A = np.array(matrix, dtype=float)
    return np.allclose(A.sum(axis=1), 1.0, atol=tol) and np.all(A >= -tol)


def classify_algebraic_structure(matrix: list[list[float]]) -> dict[str, Any]:
    """Heuristic classification of a small integer Cayley-like table."""
    A = np.array(matrix, dtype=int)
    n = A.shape[0] if A.ndim == 2 else 0
    result = {"size": n}
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        result["valid_table"] = False
        return result
    # check closure: all entries in 0..n-1
    closed = bool(np.all((A >= 0) & (A < n)))
    result["closed"] = closed
    if not closed:
        return result
    # associativity (expensive; only for small n)
    if n <= 12:
        assoc = True
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if A[A[i, j], k] != A[i, A[j, k]]:
                        assoc = False
                        break
        result["associative"] = assoc
    # identity
    identity = None
    for e in range(n):
        if np.all(A[e] == np.arange(n)) and np.all(A[:, e] == np.arange(n)):
            identity = e
            break
    result["identity"] = identity
    # inverses (if identity exists)
    if identity is not None and result.get("associative", False):
        has_inverses = True
        for i in range(n):
            if not any(A[i, j] == identity and A[j, i] == identity for j in range(n)):
                has_inverses = False
                break
        result["has_inverses"] = has_inverses
        # abelian
        result["abelian"] = bool(np.allclose(A, A.T))
    return result


def spectral_decomposition_summary(matrix: list[list[float]]) -> dict[str, Any]:
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {"error": "matrix must be square"}
    w, V = np.linalg.eig(A)
    return {
        "eigenvalues": w.tolist(),
        "is_diagonalizable": bool(np.all(np.abs(w) > 0) and np.linalg.matrix_rank(V) == A.shape[0]),
        "spectral_radius": float(max(abs(w))),
    }


__all__ = [
    "matrix_summary", "is_symmetric", "is_positive_definite", "is_stochastic",
    "classify_algebraic_structure", "spectral_decomposition_summary",
]
