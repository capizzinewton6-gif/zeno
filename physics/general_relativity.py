"""Curved spacetime, metric tensors, geodesics, and black hole physics."""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


C = CONSTANTS.value("c")
G = CONSTANTS.value("G")


def schwarzschild_radius(M: float) -> float:
    """Event-horizon radius of a non-rotating mass M."""
    return 2 * G * M / C ** 2


def schwarzschild_metric(r: sp.Symbol, rs: sp.Symbol) -> sp.Matrix:
    """Schwarzschild metric tensor in (t, r, theta, phi) coordinates."""
    diag = [-(1 - rs / r), 1 / (1 - rs / r), r ** 2, r ** 2 * sp.sin(sp.Symbol("theta")) ** 2]
    return sp.diag(*diag)


class GeodesicSolver:
    """Numerical integration of timelike geodesics in the Schwarzschild metric.

    Uses the effective-potential formulation for equatorial orbits (theta = pi/2).
    Units: set G = M = c = 1 for dimensionless study; rescale to SI on output.
    """

    def __init__(self, rs: float = 1.0):
        self.rs = rs

    def effective_potential(self, r: np.ndarray, L: float, kappa: float = 1.0) -> np.ndarray:
        """V_eff(r) for a particle with specific angular momentum L.
        kappa = 1 for massive (timelike), 0 for null."""
        return -self.rs / (2 * r) + L ** 2 / (2 * r ** 2) - self.rs * L ** 2 / (r ** 3) * kappa

    def integrate(self, r0: float, phi0: float, vr0: float, vphi0: float, L: float,
                 dt: float, n_steps: int, kappa: float = 1.0) -> np.ndarray:
        """Integrate orbit (r(t), phi(t)) using RK4 on the effective 1D problem."""
        def deriv(state):
            r, vr, phi = state
            V = self.effective_potential(np.array([r]), L, kappa)[0]
            dVdr = (self.rs / (2 * r ** 2)
                    - L ** 2 / r ** 3
                    + 3 * self.rs * L ** 2 * kappa / r ** 4)
            drdt = vr
            dvrdt = -dVdr
            dphidt = L / r ** 2
            return np.array([drdt, dvrdt, dphidt])

        traj = np.empty((n_steps + 1, 3))
        traj[0] = [r0, vr0, phi0]
        s = np.array([r0, vr0, phi0], dtype=float)
        for i in range(1, n_steps + 1):
            k1 = deriv(s)
            k2 = deriv(s + 0.5 * dt * k1)
            k3 = deriv(s + 0.5 * dt * k2)
            k4 = deriv(s + dt * k3)
            s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            traj[i] = s
        return traj


class BlackHolePhysics:
    """Schwarzschild and (basic) Kerr quantities."""

    @staticmethod
    def schwarzschild_radius(M: float) -> float:
        return 2 * G * M / C ** 2

    @staticmethod
    def hawking_temperature(M: float) -> float:
        """T_H = hbar c^3 / (8 pi G M k_B)."""
        hbar = CONSTANTS.value("hbar")
        kB = CONSTANTS.value("kB")
        return hbar * C ** 3 / (8 * math.pi * G * M * kB)

    @staticmethod
    def isco_schwarzschild(M: float) -> float:
        """Innermost stable circular orbit (6M in G=c=1 units -> 3 r_s)."""
        return 3 * BlackHolePhysics.schwarzschild_radius(M)

    @staticmethod
    def kerr_ergosphere(a: float, M: float, theta: float = math.pi / 2) -> float:
        """Ergosphere radius r_E(theta) for Kerr with spin parameter a."""
        rs = 2 * G * M / C ** 2
        return rs + math.sqrt(max(rs ** 2 / 4 - a ** 2 * math.cos(theta) ** 2, 0.0))
