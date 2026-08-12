"""Hypothesis testing, ANOVA and distribution fitting."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def descriptive_stats(data: list[float]) -> dict[str, float]:
    arr = np.array(data, dtype=float)
    return {
        "n": len(arr),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "var": float(np.var(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "q1": float(np.percentile(arr, 25)),
        "q3": float(np.percentile(arr, 75)),
    }


def t_test_one_sample(data: list[float], mu0: float) -> dict[str, Any]:
    arr = np.array(data, dtype=float)
    t, p = stats.ttest_1samp(arr, mu0)
    return {"t_statistic": float(t), "p_value": float(p), "reject_H0_at_0.05": p < 0.05}


def t_test_two_sample(a: list[float], b: list[float]) -> dict[str, Any]:
    t, p = stats.ttest_ind(a, b)
    return {"t_statistic": float(t), "p_value": float(p), "reject_H0_at_0.05": p < 0.05}


def anova_one_way(*groups: list[float]) -> dict[str, Any]:
    f, p = stats.f_oneway(*groups)
    return {"f_statistic": float(f), "p_value": float(p), "reject_H0_at_0.05": p < 0.05}


def chi_square_goodness(observed: list[int], expected: list[float] | None = None) -> dict[str, Any]:
    obs = np.array(observed, dtype=float)
    exp = np.array(expected, dtype=float) if expected else np.full_like(obs, obs.sum() / len(obs))
    chi2, p = stats.chisquare(obs, exp)
    return {"chi2_statistic": float(chi2), "p_value": float(p), "reject_H0_at_0.05": p < 0.05}


def pearson_correlation(x: list[float], y: list[float]) -> dict[str, Any]:
    r, p = stats.pearsonr(x, y)
    return {"correlation": float(r), "p_value": float(p)}


def fit_normal(data: list[float]) -> dict[str, float]:
    arr = np.array(data, dtype=float)
    mu, sigma = stats.norm.fit(arr)
    return {"mean": float(mu), "std": float(sigma)}


def kolmogorov_smirnov(data: list[float], dist: str = "norm") -> dict[str, Any]:
    arr = np.array(data, dtype=float)
    d, p = stats.kstest(arr, dist)
    return {"d_statistic": float(d), "p_value": float(p)}


__all__ = [
    "descriptive_stats", "t_test_one_sample", "t_test_two_sample",
    "anova_one_way", "chi_square_goodness", "pearson_correlation",
    "fit_normal", "kolmogorov_smirnov",
]
