"""Engineering mathematics: linear algebra, calculus, and numerical methods."""

from __future__ import annotations

import math
from typing import List

import numpy as np


class EngineeringMath:
    def solve_linear(self, A: List[List[float]], b: List[float]) -> List[float]:
        return list(np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float)))

    def eigen(self, A: List[List[float]]) -> dict:
        vals, vecs = np.linalg.eig(np.array(A, dtype=float))
        return {"eigenvalues": vals.tolist(), "eigenvectors": vecs.tolist()}

    def integrate_trapz(self, y: List[float], x: List[float]) -> float:
        return float(np.trapz(y, x))

    def derivative(self, f, x: float, h: float = 1e-5) -> float:
        return (f(x + h) - f(x - h)) / (2 * h)

    def root_bisection(self, f, a: float, b: float, tol: float = 1e-6,
                       max_iter: int = 100) -> float:
        if f(a) * f(b) >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs.")
        for _ in range(max_iter):
            c = (a + b) / 2
            if abs(f(c)) < tol:
                return c
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2

    def matrix_ops(self, A: List[List[float]]) -> dict:
        m = np.array(A, dtype=float)
        return {"determinant": float(np.linalg.det(m)),
                "inverse": np.linalg.inv(m).tolist() if np.linalg.det(m) != 0 else None}

    @staticmethod
    def factorial(n: int) -> int:
        return math.factorial(n)

    @staticmethod
    def statistics(data: List[float]) -> dict:
        arr = np.array(data, dtype=float)
        return {"mean": float(arr.mean()), "std": float(arr.std()),
                "min": float(arr.min()), "max": float(arr.max())}
