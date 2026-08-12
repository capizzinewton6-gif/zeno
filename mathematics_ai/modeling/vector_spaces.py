"""Infinite-dimensional Hilbert/Banach space transformations."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np


def l2_inner_product(u: list[float] | np.ndarray, v: list[float] | np.ndarray) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return float(np.sum(u * np.conj(v)))


def l2_norm(u: list[float] | np.ndarray) -> float:
    return float(np.sqrt(l2_inner_product(u, u)))


def orthonormalize(vectors: list[list[float]]) -> list[list[float]]:
    """Gram-Schmidt orthonormalization."""
    basis: list[np.ndarray] = []
    for v in vectors:
        w = np.array(v, dtype=float)
        for b in basis:
            w = w - l2_inner_product(w, b) * b
        n = np.linalg.norm(w)
        if n > 1e-12:
            basis.append(w / n)
    return [b.tolist() for b in basis]


def hilbert_matrix(n: int) -> list[list[float]]:
    return [[1 / (i + j + 1) for j in range(n)] for i in range(n)]


def fourier_basis_coefficients(f: Callable[[float], float], n: int = 10) -> dict[str, list[float]]:
    """Compute Fourier coefficients a_k, b_k of f on [-π, π]."""
    xs = np.linspace(-np.pi, np.pi, 1000)
    fs = np.array([f(x) for x in xs])
    a = [float(np.trapz(fs * np.cos(k * xs), xs) / np.pi) for k in range(n)]
    b = [float(np.trapz(fs * np.sin(k * xs), xs) / np.pi) for k in range(n)]
    return {"a_k": a, "b_k": b}


def operator_norm_2(A: list[list[float]]) -> float:
    """Spectral norm (largest singular value) of an operator."""
    return float(np.linalg.norm(np.array(A, dtype=float), ord=2))


def is_bounded_linear_operator(A: list[list[float]], norm_bound: float | None = None) -> bool:
    n = operator_norm_2(A)
    return n < (norm_bound if norm_bound is not None else float("inf"))


def banach_fixed_point(T: Callable[[np.ndarray], np.ndarray], x0: np.ndarray, tol: float = 1e-10, max_iter: int = 1000) -> np.ndarray | None:
    x = x0.copy()
    for _ in range(max_iter):
        nx = T(x)
        if np.linalg.norm(nx - x) < tol:
            return nx
        x = nx
    return None


__all__ = [
    "l2_inner_product", "l2_norm", "orthonormalize", "hilbert_matrix",
    "fourier_basis_coefficients", "operator_norm_2", "is_bounded_linear_operator",
    "banach_fixed_point",
]
