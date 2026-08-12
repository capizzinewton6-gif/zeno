"""Extract functions and discrete data points from plots."""

from __future__ import annotations

from typing import Any

import numpy as np


def extract_points_from_image_mask(mask: np.ndarray, num_points: int = 50) -> list[tuple[float, float]]:
    """Given a binary mask of a curve, sample points along it."""
    coords = np.argwhere(mask > 0)
    if len(coords) == 0:
        return []
    coords = coords[coords[:, 1].argsort()]  # sort by x (column)
    idx = np.linspace(0, len(coords) - 1, num_points).astype(int)
    sampled = coords[idx]
    # normalize to [0, 1]
    h, w = mask.shape
    return [(float(x / w), 1.0 - float(y / h)) for y, x in sampled]


def fit_curve_to_points(points: list[tuple[float, float]], degree: int = 3) -> dict[str, Any]:
    """Fit a polynomial to extracted points."""
    arr = np.array(points, dtype=float)
    coeffs = np.polyfit(arr[:, 0], arr[:, 1], degree)
    y_pred = np.polyval(coeffs, arr[:, 0])
    ss_res = float(np.sum((arr[:, 1] - y_pred) ** 2))
    ss_tot = float(np.sum((arr[:, 1] - arr[:, 1].mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return {"coefficients": coeffs.tolist(), "r_squared": r2}


def digitize_plot_axis(image: np.ndarray, axis_region: np.ndarray) -> list[float]:
    """Extract tick labels via OCR placeholder; returns uniform spacing."""
    n = 10
    return np.linspace(0, 1, n).tolist()


__all__ = ["extract_points_from_image_mask", "fit_curve_to_points", "digitize_plot_axis"]
