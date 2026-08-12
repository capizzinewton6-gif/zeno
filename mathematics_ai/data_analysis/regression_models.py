"""Parametric, non-parametric and symbolic regression."""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp


def linear_regression(x: list[float], y: list[float]) -> dict[str, Any]:
    arr_x = np.array(x, dtype=float)
    arr_y = np.array(y, dtype=float)
    n = len(arr_x)
    slope, intercept = np.polyfit(arr_x, arr_y, 1)
    y_pred = slope * arr_x + intercept
    ss_res = float(np.sum((arr_y - y_pred) ** 2))
    ss_tot = float(np.sum((arr_y - arr_y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {"slope": float(slope), "intercept": float(intercept), "r_squared": r2}


def polynomial_regression(x: list[float], y: list[float], degree: int = 2) -> dict[str, Any]:
    coeffs = np.polyfit(np.array(x, dtype=float), np.array(y, dtype=float), degree)
    return {"coefficients": coeffs.tolist(), "degree": degree}


def logistic_regression(x: list[float], y: list[int], lr: float = 0.01, epochs: int = 1000) -> dict[str, Any]:
    """Gradient-descent logistic regression."""
    arr_x = np.array(x, dtype=float).reshape(-1, 1)
    arr_y = np.array(y, dtype=float)
    arr_x = np.hstack([np.ones((len(arr_x), 1)), arr_x])
    weights = np.zeros(arr_x.shape[1])
    for _ in range(epochs):
        z = arr_x @ weights
        p = 1 / (1 + np.exp(-z))
        grad = arr_x.T @ (p - arr_y) / len(arr_y)
        weights -= lr * grad
    return {"weights": weights.tolist()}


def kernel_regression(x: list[float], y: list[float], x_eval: list[float], bandwidth: float = 1.0) -> list[float]:
    """Nadaraya-Watson kernel regression."""
    arr_x = np.array(x, dtype=float)
    arr_y = np.array(y, dtype=float)
    preds = []
    for xe in x_eval:
        w = np.exp(-((arr_x - xe) ** 2) / (2 * bandwidth ** 2))
        preds.append(float(np.sum(w * arr_y) / np.sum(w)))
    return preds


def symbolic_regression(x: list[float], y: list[float], max_terms: int = 3) -> dict[str, Any]:
    """Find a simple symbolic expression via polynomial fitting (heuristic)."""
    arr_x = np.array(x, dtype=float)
    arr_y = np.array(y, dtype=float)
    for deg in range(1, max_terms + 2):
        coeffs = np.polyfit(arr_x, arr_y, deg)
        y_pred = np.polyval(coeffs, arr_x)
        ss_res = float(np.sum((arr_y - y_pred) ** 2))
        ss_tot = float(np.sum((arr_y - arr_y.mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        if r2 > 0.99:
            t = sp.Symbol("x")
            expr = sum(sp.Rational(float(c)) * t ** (deg - i) for i, c in enumerate(coeffs))
            return {"expression": str(sp.expand(expr)), "r_squared": r2}
    return {"expression": None, "r_squared": r2}


__all__ = [
    "linear_regression", "polynomial_regression", "logistic_regression",
    "kernel_regression", "symbolic_regression",
]
