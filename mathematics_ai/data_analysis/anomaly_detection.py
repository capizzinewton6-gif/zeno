"""Outlier, topological data analysis (TDA) and pattern anomalies."""

from __future__ import annotations

from typing import Any

import numpy as np


def z_score_outliers(data: list[float], threshold: float = 3.0) -> list[int]:
    arr = np.array(data, dtype=float)
    z = (arr - arr.mean()) / arr.std() if arr.std() > 0 else np.zeros_like(arr)
    return [i for i, v in enumerate(z) if abs(v) > threshold]


def iqr_outliers(data: list[float], factor: float = 1.5) -> list[int]:
    arr = np.array(data, dtype=float)
    q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
    iqr = q3 - q1
    lower, upper = q1 - factor * iqr, q3 + factor * iqr
    return [i for i, v in enumerate(arr) if v < lower or v > upper]


def isolation_forest_approx(data: list[list[float]], n_trees: int = 100, sample_size: int = 256) -> list[float]:
    """Approximate anomaly scores via random splits (single-feature simplification)."""
    arr = np.array(data, dtype=float)
    n = len(arr)
    scores = np.zeros(n)
    rng = np.random.default_rng(42)
    for _ in range(n_trees):
        idx = rng.choice(n, min(sample_size, n), replace=False)
        for col in range(arr.shape[1]):
            mins, maxs = arr[idx, col].min(), arr[idx, col].max()
            split = rng.uniform(mins, maxs)
            scores += np.abs(arr[:, col] - split)
    scores /= (n_trees * arr.shape[1])
    # normalize: lower = more anomalous
    return ((scores - scores.min()) / (scores.max() - scores.min() + 1e-12)).tolist()


def persistence_diagram_simple(distance_matrix: np.ndarray) -> dict[int, list[tuple[float, float]]]:
    """Simplified persistence diagram (H0 only) from a distance matrix."""
    from mathematics_ai.topology_geometry.homology_engine import persistent_homology_lifetimes
    return persistent_homology_lifetimes(distance_matrix, max_dim=1)


def detect_pattern_breaks(data: list[float], window: int = 10, threshold: float = 2.0) -> list[int]:
    """Detect points where local mean changes abruptly."""
    arr = np.array(data, dtype=float)
    breaks = []
    for i in range(window, len(arr) - window):
        left = arr[i - window:i]
        right = arr[i:i + window]
        if abs(left.mean() - right.mean()) > threshold * (left.std() + 1e-9):
            breaks.append(i)
    return breaks


__all__ = [
    "z_score_outliers", "iqr_outliers", "isolation_forest_approx",
    "persistence_diagram_simple", "detect_pattern_breaks",
]
