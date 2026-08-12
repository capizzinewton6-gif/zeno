"""Surface waves, 2D potentials, and planar stress tensors."""

from __future__ import annotations

import numpy as np

from calculations.field_solvers import FieldSolvers


class Fields2D:
    """2D scalar and vector field utilities."""

    @staticmethod
    def gaussian_potential_2d(X: np.ndarray, Y: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        return np.exp(-(X ** 2 + Y ** 2) / (2 * sigma ** 2))

    @staticmethod
    def surface_wave(X: np.ndarray, Y: np.ndarray, kx: float, ky: float, t: float = 0.0) -> np.ndarray:
        return np.sin(kx * X + ky * Y - t)

    @staticmethod
    def stress_tensor_2d(sigma_xx: np.ndarray, sigma_yy: np.ndarray, sigma_xy: np.ndarray) -> np.ndarray:
        """Stack components into a (nx, ny, 2, 2) planar stress tensor."""
        nx, ny = sigma_xx.shape
        T = np.zeros((nx, ny, 2, 2))
        T[..., 0, 0] = sigma_xx
        T[..., 1, 1] = sigma_yy
        T[..., 0, 1] = sigma_xy
        T[..., 1, 0] = sigma_xy
        return T
