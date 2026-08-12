"""Eigenvalues, SVD and matrix operations (numeric, NumPy-based)."""

from __future__ import annotations

from typing import Any

import numpy as np


def eigenvalues(matrix: list[list[float]]) -> list[complex]:
    return np.linalg.eigvals(np.array(matrix, dtype=float)).tolist()


def eigendecomposition(matrix: list[list[float]]) -> dict[str, list]:
    w, V = np.linalg.eig(np.array(matrix, dtype=float))
    return {"eigenvalues": w.tolist(), "eigenvectors": V.tolist()}


def svd(matrix: list[list[float]]) -> dict[str, list]:
    U, S, Vt = np.linalg.svd(np.array(matrix, dtype=float))
    return {"U": U.tolist(), "singular_values": S.tolist(), "Vt": Vt.tolist()}


def determinant(matrix: list[list[float]]) -> float:
    return float(np.linalg.det(np.array(matrix, dtype=float)))


def inverse(matrix: list[list[float]]) -> list[list[float]]:
    return np.linalg.inv(np.array(matrix, dtype=float)).tolist()


def pseudo_inverse(matrix: list[list[float]]) -> list[list[float]]:
    return np.linalg.pinv(np.array(matrix, dtype=float)).tolist()


def qr(matrix: list[list[float]]) -> dict[str, list]:
    Q, R = np.linalg.qr(np.array(matrix, dtype=float))
    return {"Q": Q.tolist(), "R": R.tolist()}


def lu(matrix: list[list[float]]) -> dict[str, list]:
    import scipy.linalg
    P, L, U = scipy.linalg.lu(np.array(matrix, dtype=float))
    return {"P": P.tolist(), "L": L.tolist(), "U": U.tolist()}


def matrix_power(matrix: list[list[float]], n: int) -> list[list[float]]:
    return np.linalg.matrix_power(np.array(matrix, dtype=float), n).tolist()


def norm(matrix: list[list[float]], ord: Any = None) -> float:
    return float(np.linalg.norm(np.array(matrix, dtype=float), ord=ord))


def condition_number(matrix: list[list[float]]) -> float:
    return float(np.linalg.cond(np.array(matrix, dtype=float)))


def solve_linear(A: list[list[float]], b: list[float]) -> list[float]:
    return np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float)).tolist()


def least_squares(A: list[list[float]], b: list[float]) -> dict[str, Any]:
    x, residuals, rank, sv = np.linalg.lstsq(np.array(A, dtype=float), np.array(b, dtype=float), rcond=None)
    return {"solution": x.tolist(), "residuals": residuals.tolist(), "rank": int(rank), "singular_values": sv.tolist()}


__all__ = [
    "eigenvalues", "eigendecomposition", "svd", "determinant", "inverse",
    "pseudo_inverse", "qr", "lu", "matrix_power", "norm", "condition_number",
    "solve_linear", "least_squares",
]
