"""Analyze knot diagrams and topological shape renders."""

from __future__ import annotations

from typing import Any

import numpy as np


def count_crossings_from_projection(curve_xy: list[tuple[float, float]], closed: bool = True) -> int:
    """Count self-intersections of a 2D projection (knot diagram)."""
    n = len(curve_xy)
    pts = curve_xy + ([curve_xy[0]] if closed else [])
    count = 0
    for i in range(n - 1):
        for j in range(i + 2, n - 1):
            if _segments_intersect(pts[i], pts[i + 1], pts[j], pts[j + 1]):
                count += 1
    return count


def _ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_intersect(a, b, c, d) -> bool:
    return (_ccw(a, c, d) * _ccw(b, c, d) <= 0) and (_ccw(a, b, c) * _ccw(a, b, d) <= 0)


def trefoil_projection(t: np.ndarray) -> list[tuple[float, float]]:
    """2D projection of a trefoil knot."""
    return [(float(np.sin(t_i) + 2 * np.sin(2 * t_i)), float(np.cos(t_i) - 2 * np.cos(2 * t_i))) for t_i in t]


def classify_shape_from_silhouette(silhouette: list[tuple[float, float]]) -> str:
    """Heuristic shape classification from a closed silhouette."""
    n = len(silhouette)
    crossings = count_crossings_from_projection(silhouette)
    if crossings == 0:
        # convexity test
        pts = np.array(silhouette)
        c = pts.mean(axis=0)
        dists = np.linalg.norm(pts - c, axis=1)
        if np.std(dists) / (np.mean(dists) + 1e-9) < 0.1:
            return "circle"
        return "polygon"
    if crossings <= 3:
        return "trefoil"
    if crossings == 4:
        return "figure_eight"
    return "composite_knot"


__all__ = ["count_crossings_from_projection", "trefoil_projection", "classify_shape_from_silhouette"]
