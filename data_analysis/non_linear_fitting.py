"""Levenberg-Marquardt fitting to theoretical physical curves."""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy.optimize import curve_fit


class NonLinearFitting:
    """Levenberg-Marquardt wrapper around scipy.optimize.curve_fit."""

    @staticmethod
    def fit(model: Callable, x: np.ndarray, y: np.ndarray, p0: list[float] | None = None,
            sigma: np.ndarray | None = None, absolute_sigma: bool = False) -> dict:
        popt, pcov = curve_fit(model, x, y, p0=p0, sigma=sigma, absolute_sigma=absolute_sigma, maxfev=10000)
        perr = np.sqrt(np.diag(pcov))
        return {"params": popt.tolist(), "covariance": pcov.tolist(), "errors": perr.tolist()}

    @staticmethod
    def residuals(model: Callable, x: np.ndarray, y: np.ndarray, params: np.ndarray) -> np.ndarray:
        return np.asarray(y, dtype=float) - np.array([model(xi, *params) for xi in x])

    @staticmethod
    def r_squared(model: Callable, x: np.ndarray, y: np.ndarray, params: np.ndarray) -> float:
        residuals = NonLinearFitting.residuals(model, x, y, params)
        ss_res = float(np.sum(residuals ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        return 1 - ss_res / ss_tot
