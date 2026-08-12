"""3D manifolds, knot projections and spatial geometry."""

from __future__ import annotations

from typing import Any

import numpy as np


def trefoil_knot(t: list[float]) -> list[tuple[float, float, float]]:
    """Parametric trefoil knot."""
    pts = []
    for ti in t:
        x = np.sin(ti) + 2 * np.sin(2 * ti)
        y = np.cos(ti) - 2 * np.cos(2 * ti)
        z = -np.sin(3 * ti)
        pts.append((x, y, z))
    return pts


def figure_eight_knot(t: list[float]) -> list[tuple[float, float, float]]:
    """Parametric figure-eight knot."""
    pts = []
    for ti in t:
        x = (2 + np.cos(2 * ti)) * np.cos(3 * ti)
        y = (2 + np.cos(2 * ti)) * np.sin(3 * ti)
        z = np.sin(4 * ti)
        pts.append((x, y, z))
    return pts


def sphere_volume(radius: float) -> float:
    return (4 / 3) * np.pi * radius ** 3


def sphere_surface_area(radius: float) -> float:
    return 4 * np.pi * radius ** 2


def torus_volume(R: float, r: float) -> float:
    return 2 * np.pi ** 2 * R * r ** 2


def torus_surface_area(R: float, r: float) -> float:
    return 4 * np.pi ** 2 * R * r


def solid_of_revolution(f, a: float, b: float, n: int = 1000) -> float:
    """Volume of the solid obtained by rotating y = f(x) around the x-axis."""
    xs = np.linspace(a, b, n)
    ys = np.array([f(x) for x in xs])
    return float(np.trapz(np.pi * ys ** 2, xs))


def gauss_curvature_principal(r1: float, r2: float) -> float:
    """Gaussian curvature from principal radii K = 1/(r1*r2)."""
    return 1.0 / (r1 * r2)


def distance_3d(p1, p2) -> float:
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))


__all__ = [
    "trefoil_knot", "figure_eight_knot", "sphere_volume", "sphere_surface_area",
    "torus_volume", "torus_surface_area", "solid_of_revolution",
    "gauss_curvature_principal", "distance_3d",
]
