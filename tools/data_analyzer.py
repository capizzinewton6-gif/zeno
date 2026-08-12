"""Analyze raw experimental data and multidimensional field grids."""

from __future__ import annotations

import numpy as np


class DataAnalyzer:
    """Basic reductions over experimental/field data arrays."""

    @staticmethod
    def reduce_stats(data: np.ndarray) -> dict[str, float]:
        a = np.asarray(data, dtype=float)
        return {
            "mean": float(np.mean(a)),
            "median": float(np.median(a)),
            "std": float(np.std(a, ddof=1)) if a.size > 1 else 0.0,
            "min": float(np.min(a)),
            "max": float(np.max(a)),
            "n": int(a.size),
        }

    @staticmethod
    def grid_slice(grid: np.ndarray, axis: int, index: int) -> np.ndarray:
        idx = [slice(None)] * grid.ndim
        idx[axis] = index
        return grid[tuple(idx)]

    @staticmethod
    def histogram(data: np.ndarray, bins: int = 30):
        return np.histogram(np.asarray(data, dtype=float).ravel(), bins=bins)
