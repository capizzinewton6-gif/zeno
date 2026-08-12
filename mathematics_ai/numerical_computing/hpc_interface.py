"""Parallel linear algebra / BLAS-LAPACK interface (NumPy/SciPy-backed).

A real GPU/cluster binding is out of scope in this environment; this module
exposes a clean interface backed by NumPy/SciPy dense/sparse routines so the
rest of the system can call it uniformly.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import scipy.linalg
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def eigvals(matrix: Any) -> list[complex]:
    A = np.asarray(matrix, dtype=float)
    return scipy.linalg.eigvals(A).tolist()


def svd(matrix: Any) -> dict[str, list]:
    U, S, Vt = scipy.linalg.svd(np.asarray(matrix, dtype=float))
    return {"U": U.tolist(), "singular_values": S.tolist(), "Vt": Vt.tolist()}


def lu_factor(matrix: Any) -> dict[str, Any]:
    lu, piv = scipy.linalg.lu_factor(np.asarray(matrix, dtype=float))
    return {"lu": lu.tolist(), "piv": piv.tolist()}


def solve(A: Any, b: Any) -> list[float]:
    return scipy.linalg.solve(np.asarray(A, dtype=float), np.asarray(b, dtype=float)).tolist()


def sparse_eigenvalues(matrix: Any, k: int = 6) -> list[complex]:
    A = sp.csr_matrix(matrix)
    return spla.eigs(A, k=k, return_eigenvectors=False).tolist()


def cholesky(matrix: Any) -> list[list[float]]:
    return scipy.linalg.cholesky(np.asarray(matrix, dtype=float)).tolist()


def qr(matrix: Any) -> dict[str, list]:
    Q, R = scipy.linalg.qr(np.asarray(matrix, dtype=float))
    return {"Q": Q.tolist(), "R": R.tolist()}


def schur(matrix: Any) -> dict[str, list]:
    T, Z = scipy.linalg.schur(np.asarray(matrix, dtype=float))
    return {"T": T.tolist(), "Z": Z.tolist()}


__all__ = [
    "eigvals", "svd", "lu_factor", "solve", "sparse_eigenvalues",
    "cholesky", "qr", "schur",
]
