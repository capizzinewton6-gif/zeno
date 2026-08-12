"""Error analysis, covariance matrices, and experimental noise modeling."""

from __future__ import annotations

import numpy as np


class UncertaintyPropagator:
    """Gaussian uncertainty propagation and covariance-based error analysis."""

    @staticmethod
    def linear(jacobian: np.ndarray, cov: np.ndarray) -> float:
        """sigma_y = sqrt(J Cov J^T)."""
        return float(np.sqrt(max(jacobian @ cov @ jacobian.T, 0.0)))

    @staticmethod
    def combine_independent(uncertainties: list[float]) -> float:
        """Quadrature combination of independent uncertainties."""
        return float(np.sqrt(np.sum(np.square(uncertainties))))

    @staticmethod
    def relative(sigma: float, value: float) -> float:
        return sigma / abs(value) if value != 0 else float("inf")

    @staticmethod
    def covariance_from_samples(samples: np.ndarray) -> np.ndarray:
        return np.cov(np.asarray(samples, dtype=float), rowvar=False)

    @staticmethod
    def confidence_interval(mean: float, sigma: float, level: float = 0.95) -> tuple[float, float]:
        """Symmetric CI assuming Gaussian errors (z ~ 1.96 for 95%)."""
        from scipy.stats import norm
        z = norm.ppf(0.5 + level / 2)
        return mean - z * sigma, mean + z * sigma
