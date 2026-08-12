"""Dynamic compass-and-straightedge geometric construction."""

from __future__ import annotations

from typing import Any

import numpy as np


def perpendicular_bisector(p1: tuple[float, float], p2: tuple[float, float]) -> dict[str, Any]:
    """Return midpoint and direction of the perpendicular bisector of segment p1-p2."""
    p1 = np.array(p1)
    p2 = np.array(p2)
    mid = (p1 + p2) / 2
    direction = p2 - p1
    perp = np.array([-direction[1], direction[0]])
    norm = np.linalg.norm(perp)
    perp = perp / norm if norm > 0 else perp
    return {"midpoint": mid.tolist(), "direction": perp.tolist()}


def angle_bisector(p1, vertex, p2) -> tuple[float, float]:
    """Direction of the internal angle bisector at vertex."""
    v1 = np.array(p1) - np.array(vertex)
    v2 = np.array(p2) - np.array(vertex)
    v1 = v1 / (np.linalg.norm(v1) + 1e-12)
    v2 = v2 / (np.linalg.norm(v2) + 1e-12)
    bisector = v1 + v2
    return tuple(bisector / (np.linalg.norm(bisector) + 1e-12))


def circle_through_three_points(p1, p2, p3) -> dict[str, Any]:
    """Circumcircle of a triangle given by three points."""
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < 1e-12:
        return {"center": None, "radius": None, "note": "collinear points"}
    ux = ((a[0] ** 2 + a[1] ** 2) * (b[1] - c[1]) + (b[0] ** 2 + b[1] ** 2) * (c[1] - a[1]) + (c[0] ** 2 + c[1] ** 2) * (a[1] - b[1])) / d
    uy = ((a[0] ** 2 + a[1] ** 2) * (c[0] - b[0]) + (b[0] ** 2 + b[1] ** 2) * (a[0] - c[0]) + (c[0] ** 2 + c[1] ** 2) * (b[0] - a[0])) / d
    center = np.array([ux, uy])
    radius = float(np.linalg.norm(center - a))
    return {"center": center.tolist(), "radius": radius}


def construct_equilateral_triangle(side: float) -> list[tuple[float, float]]:
    s = side
    return [(0, 0), (s, 0), (s / 2, s * np.sqrt(3) / 2)]


def construct_regular_polygon(n: int, radius: float = 1.0) -> list[tuple[float, float]]:
    return [(float(radius * np.cos(2 * np.pi * k / n)), float(radius * np.sin(2 * np.pi * k / n))) for k in range(n)]


def line_line_intersection(p1, p2, p3, p4) -> tuple[float, float] | None:
    """Intersection of two lines, each given by two points."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


__all__ = [
    "perpendicular_bisector", "angle_bisector", "circle_through_three_points",
    "construct_equilateral_triangle", "construct_regular_polygon", "line_line_intersection",
]
