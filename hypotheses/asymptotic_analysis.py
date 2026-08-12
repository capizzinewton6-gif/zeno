"""Near-field, far-field, thermodynamic, and non-relativistic limits."""

from __future__ import annotations

import numpy as np
import sympy as sp


class AsymptoticAnalysis:
    """Compute limiting behaviors of physical expressions."""

    @staticmethod
    def series(expr: sp.Expr, var: sp.Symbol, order: int = 2, x0: float = 0) -> sp.Expr:
        return sp.series(expr, var, x0, order + 1).removeO()

    @staticmethod
    def nonrelativistic_energy(E: float, m: float, c: float = 3e8) -> float:
        """E = gamma m c^2 -> m c^2 + (1/2) m v^2 for v << c."""
        v = c * np.sqrt(max(1 - (m * c ** 2 / E) ** 2, 0.0))
        return 0.5 * m * v ** 2

    @staticmethod
    def far_field(r: float, wavelength: float) -> bool:
        """Fraunhofer far-field condition: r >> D^2 / lambda (D ~ characteristic size)."""
        return r * wavelength > 1.0

    @staticmethod
    def near_field(r: float, wavelength: float) -> bool:
        return r < wavelength / (2 * np.pi)

    @staticmethod
    def thermodynamic_limit(N: int) -> dict:
        """N -> infinity with N/V fixed: fluctuations ~ 1/sqrt(N)."""
        return {"N": N, "relative_fluctuation": 1.0 / np.sqrt(N), "extensive": True}
