"""Chisq minimization, maximum likelihood, and signal significance."""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
from scipy.optimize import minimize, brentq
from scipy.stats import norm


class ExperimentalStatistics:
    """Frequentist fit and significance utilities."""

    @staticmethod
    def chi_squared(params: np.ndarray, model: Callable, x: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> float:
        ym = np.array([model(x[i], params) for i in range(len(x))], dtype=float)
        return float(np.sum(((y - ym) / sigma) ** 2))

    @staticmethod
    def fit(model: Callable, x0: np.ndarray, x: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> dict:
        res = minimize(lambda p: ExperimentalStatistics.chi_squared(p, model, x, y, sigma),
                       np.asarray(x0, dtype=float), method="Nelder-Mead")
        dof = max(len(x) - len(x0), 1)
        return {"params": res.x.tolist(), "chi2": res.fun, "reduced_chi2": res.fun / dof, "dof": dof}

    @staticmethod
    def maximum_likelihood(log_lik: Callable, x0: np.ndarray) -> dict:
        res = minimize(lambda p: -log_lik(p), np.asarray(x0, dtype=float), method="Nelder-Mead")
        return {"mle_params": res.x.tolist(), "log_likelihood": -res.fun}

    @staticmethod
    def significance_SSB(signal: float, background: float, sigma_b: float = 0.0) -> float:
        """Discovery significance n*sigma: S / sqrt(B + sigma_b^2)."""
        return float(signal / math.sqrt(max(background + sigma_b ** 2, 1e-30)))

    @staticmethod
    def p_value(z: float) -> float:
        return float(2 * (1 - norm.cdf(abs(z))))

    @staticmethod
    def confidence_interval_curve(level: float = 0.95) -> float:
        return float(norm.ppf(0.5 + level / 2))
