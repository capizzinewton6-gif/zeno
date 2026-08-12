"""Stellar evolution, orbital dynamics, FLRW metric, and dark energy."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


G = CONSTANTS.value("G")
C = CONSTANTS.value("c")
KB = CONSTANTS.value("kB")


class OrbitalDynamics:
    """Keplerian two-body orbits."""

    @staticmethod
    def period(a: float, M: float) -> float:
        """Kepler's third law: T = 2 pi sqrt(a^3 / (G M))."""
        return 2 * math.pi * math.sqrt(a ** 3 / (G * M))

    @staticmethod
    def vis_viva(r: float, a: float, M: float) -> float:
        return math.sqrt(G * M * (2 / r - 1 / a))

    @staticmethod
    def eccentric_anomaly_series(M_anom: float, e: float, tol: float = 1e-10, max_iter: int = 50) -> float:
        """Solve Kepler's equation M = E - e sin E by Newton's method."""
        E = M_anom
        for _ in range(max_iter):
            f = E - e * math.sin(E) - M_anom
            fp = 1 - e * math.cos(E)
            dE = -f / fp
            E += dE
            if abs(dE) < tol:
                break
        return E

    @staticmethod
    def orbit_geometry(a: float, e: float, n_points: int = 360) -> np.ndarray:
        """Return (x, y) of an elliptical orbit."""
        theta = np.linspace(0, 2 * math.pi, n_points)
        r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
        return np.vstack([r * np.cos(theta), r * np.sin(theta)]).T


class StellarStructure:
    """Polytropes and the Lane-Emden equation."""

    @staticmethod
    def lane_emden_solve(n: float = 3.0, n_steps: int = 2000) -> np.ndarray:
        """Integrate (1/x^2) d/dx(x^2 dtheta/dx) = -theta^n from x=0."""
        dx = 0.01
        xi = np.arange(0, n_steps) * dx
        theta = np.zeros_like(xi)
        dtheta = np.zeros_like(xi)
        theta[0] = 1.0
        dtheta[0] = 0.0
        for i in range(1, n_steps):
            x = xi[i - 1]
            th = theta[i - 1]
            dth = dtheta[i - 1]
            d2th = -(th ** n) - (2 / x) * dth if x > 0 else -th ** n
            dtheta[i] = dth + d2th * dx
            theta[i] = th + dth * dx
            if theta[i] <= 0:
                theta[i:] = 0.0
                break
        return np.vstack([xi, theta]).T


class Cosmology:
    """FLRW metric and Friedmann equations."""

    H0 = 67.4e3 / 3.0856775814913673e22  # H0 in s^-1 (~2.18e-18)

    def __init__(self, Omega_m: float = 0.315, Omega_Lambda: float = 0.685, Omega_r: float = 9.0e-5):
        self.Omega_m = Omega_m
        self.Omega_Lambda = Omega_Lambda
        self.Omega_r = Omega_r
        self.Omega_k = 1.0 - (Omega_m + Omega_Lambda + Omega_r)

    def hubble(self, z: float) -> float:
        E2 = (self.Omega_r * (1 + z) ** 4
              + self.Omega_m * (1 + z) ** 3
              + self.Omega_k * (1 + z) ** 2
              + self.Omega_Lambda)
        return self.H0 * math.sqrt(max(E2, 0.0))

    def comoving_distance(self, z: float, n_steps: int = 1000) -> float:
        """Integral of c/H(z') dz' from 0 to z."""
        zs = np.linspace(0, z, n_steps)
        Hz = np.array([self.hubble(zz) for zz in zs])
        integrand = C / Hz
        return float(np.trapz(integrand, zs))

    def luminosity_distance(self, z: float) -> float:
        return (1 + z) * self.comoving_distance(z)

    def age_of_universe(self, n_steps: int = 10000) -> float:
        """t_0 = integral_0^inf dz / ((1+z) H(z))."""
        z_max = 1e4
        zs = np.linspace(0, z_max, n_steps)
        Hz = np.array([self.hubble(zz) for zz in zs])
        integrand = 1.0 / ((1 + zs) * Hz)
        return float(np.trapz(integrand, zs))
