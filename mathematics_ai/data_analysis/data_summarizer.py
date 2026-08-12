"""Summary statistics, moments and entropy calculation."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def summary_statistics(data: list[float]) -> dict[str, float]:
    arr = np.array(data, dtype=float)
    return {
        "n": len(arr),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "mode": float(np.bincount(arr.astype(int)).argmax()) if np.allclose(arr, arr.astype(int)) else float("nan"),
        "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
        "variance": float(arr.var(ddof=1)) if len(arr) > 1 else 0.0,
        "min": float(arr.min()),
        "max": float(arr.max()),
        "range": float(arr.max() - arr.min()),
        "sum": float(arr.sum()),
    }


def moments(data: list[float], max_order: int = 4) -> dict[str, float]:
    arr = np.array(data, dtype=float)
    mu = arr.mean()
    std = arr.std(ddof=1) if len(arr) > 1 else 1.0
    moments = {}
    for k in range(1, max_order + 1):
        if k <= 2:
            moments[f"moment_{k}"] = float(np.mean((arr - mu) ** k))
        else:
            moments[f"moment_{k}"] = float(np.mean(((arr - mu) / std) ** k))
    # rename standardized names
    if "moment_3" in moments:
        moments["skewness"] = moments["moment_3"]
    if "moment_4" in moments:
        moments["kurtosis"] = moments["moment_4"] - 3  # excess kurtosis
    return moments


def shannon_entropy(probs: list[float]) -> float:
    p = np.array(probs, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def entropy_from_data(data: list[float], bins: int = 10) -> float:
    arr = np.array(data, dtype=float)
    hist, _ = np.histogram(arr, bins=bins, density=True)
    hist = hist[hist > 0]
    bin_width = (arr.max() - arr.min()) / bins
    return float(-np.sum(hist * bin_width * np.log2(hist * bin_width + 1e-12)))


def gini_coefficient(data: list[float]) -> float:
    arr = np.sort(np.array(data, dtype=float))
    n = len(arr)
    cumsum = np.cumsum(arr)
    return float((2 * np.sum((np.arange(1, n + 1)) * arr)) / (n * cumsum[-1]) - (n + 1) / n) if cumsum[-1] > 0 else 0.0


__all__ = ["summary_statistics", "moments", "shannon_entropy", "entropy_from_data", "gini_coefficient"]
