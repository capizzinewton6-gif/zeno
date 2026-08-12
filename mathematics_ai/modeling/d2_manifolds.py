"""Complex planes, surfaces and graphs."""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp


def complex_plane_grid(xmin: float = -2, xmax: float = 2, ymin: float = -2, ymax: float = 2, n: int = 20) -> list[list[complex]]:
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    return [[complex(xi, yi) for xi in x] for yi in y]


def riemann_sphere_stereographic(z: complex) -> tuple[float, float, float]:
    """Stereographic projection of z in C onto the Riemann sphere."""
    denom = 1 + abs(z) ** 2
    return (2 * z.real / denom, 2 * z.imag / denom, (abs(z) ** 2 - 1) / denom)


def torus_point(u: float, v: float, R: float = 2.0, r: float = 0.7) -> tuple[float, float, float]:
    """Parametric point on a torus."""
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return (x, y, z)


def surface_area_parametric(fu: Any, fv: Any, fw: Any, u_range: tuple[float, float], v_range: tuple[float, float], n: int = 50) -> float:
    """Approximate the area of a parametric surface via triangulation."""
    u = np.linspace(*u_range, n)
    v = np.linspace(*v_range, n)
    U, V = np.meshgrid(u, v)
    X = np.vectorize(fu)(U, V)
    Y = np.vectorize(fv)(U, V)
    Z = np.vectorize(fw)(U, V)
    # sum triangle areas
    area = 0.0
    for i in range(n - 1):
        for j in range(n - 1):
            p1 = np.array([X[i, j], Y[i, j], Z[i, j]])
            p2 = np.array([X[i + 1, j], Y[i + 1, j], Z[i + 1, j]])
            p3 = np.array([X[i, j + 1], Y[i, j + 1], Z[i, j + 1]])
            p4 = np.array([X[i + 1, j + 1], Y[i + 1, j + 1], Z[i + 1, j + 1]])
            area += 0.5 * np.linalg.norm(np.cross(p2 - p1, p3 - p1))
            area += 0.5 * np.linalg.norm(np.cross(p3 - p2, p4 - p2))
    return float(area)


def graph_adjacency_matrix(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    A = [[0] * n for _ in range(n)]
    for i, j in edges:
        A[i][j] = A[j][i] = 1
    return A


__all__ = [
    "complex_plane_grid", "riemann_sphere_stereographic", "torus_point",
    "surface_area_parametric", "graph_adjacency_matrix",
]
