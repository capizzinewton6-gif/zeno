"""Calculate mean, variance, systematic errors, and confidence intervals."""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


class DataSummarizer:
    """Summary statistics for experimental datasets."""

    @staticmethod
    def summary(data: np.ndarray) -> dict:
        d = np.asarray(data, dtype=float)
        return {
            "n": int(len(d)),
            "mean": float(np.mean(d)),
            "median": float(np.median(d)),
            "std": float(np.std(d, ddof=1)) if len(d) > 1 else 0.0,
            "variance": float(np.var(d, ddof=1)) if len(d) > 1 else 0.0,
            "min": float(np.min(d)),
            "max": float(np.max(d)),
            "skewness": float(stats.skew(d)) if len(d) > 2 else 0.0,
            "kurtosis": float(stats.kurtosis(d)) if len(d) > 3 else 0.0,
        }

    @staticmethod
    def systematic_error(values: np.ndarray, reference: float) -> float:
        return float(np.mean(np.asarray(values, dtype=float)) - reference)

    @staticmethod
    def confidence_interval(data: np.ndarray, level: float = 0.95) -> tuple[float, float]:
        d = np.asarray(data, dtype=float)
        n = len(d)
        mean = np.mean(d)
        sem = np.std(d, ddof=1) / math.sqrt(n) if n > 1 else 0.0
        h = sem * stats.t.ppf((1 + level) / 2, df=max(n - 1, 1))
        return float(mean - h), float(mean + h)

    @staticmethod
    def weighted_mean(values: np.ndarray, uncertainties: np.ndarray) -> dict:
        v = np.asarray(values, dtype=float)
        u = np.asarray(uncertainties, dtype=float)
        w = 1.0 / np.where(u > 0, u ** 2, 1e-30)
        wm = float(np.sum(w * v) / np.sum(w))
        sigma = float(1.0 / math.sqrt(np.sum(w)))
        return {"weighted_mean": wm, "uncertainty": sigma}
