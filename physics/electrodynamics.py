"""Maxwell equations, electromagnetic waves, and relativistic electrodynamics."""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


C = CONSTANTS.value("c")
EPS0 = CONSTANTS.value("eps0")
MU0 = CONSTANTS.value("mu0")


class MaxwellEquations:
    """Symbolic and differential-form statements of Maxwell's equations."""

    @staticmethod
    def differential_forms() -> dict[str, sp.Expr]:
        rho, t = sp.symbols("rho t")
        E = sp.Function("E")
        B = sp.Function("B")
        J = sp.Function("J")
        return {
            "Gauss_E": sp.Eq(sp.divergence_from_del(E), rho / EPS0),
            "Gauss_B": sp.Eq(sp.divergence_from_del(B), 0),
            "Faraday": sp.Eq(sp.del_cross_op(B).subs(t, t), -sp.diff(E, t)),
            "Ampere_Maxwell": sp.Eq(sp.del_cross_op(B), MU0 * J + MU0 * EPS0 * sp.diff(E, t)),
        }

    @staticmethod
    def wave_equation_1d() -> sp.Eq:
        x, t, v = sp.symbols("x t v")
        E = sp.Function("E")(x, t)
        return sp.Eq(sp.diff(E, x, 2) - (1 / v ** 2) * sp.diff(E, t, 2), 0)

    @staticmethod
    def speed_of_light() -> float:
        return 1.0 / math.sqrt(EPS0 * MU0)


class ElectromagneticWaves:
    """Plane-wave solutions and Poynting vector."""

    @staticmethod
    def plane_wave_E(E0: float, k: np.ndarray, omega: float, r: np.ndarray, t: float) -> np.ndarray:
        phase = np.dot(k, r) - omega * t
        return E0 * np.exp(1j * phase)

    @staticmethod
    def poynting(E: np.ndarray, B: np.ndarray) -> np.ndarray:
        return (1 / MU0) * np.cross(E, np.real(B))

    @staticmethod
    def intensity(E0: float) -> float:
        return 0.5 * C * EPS0 * E0 ** 2

    @staticmethod
    def radiation_pressure(E0: float, absorbing: bool = True) -> float:
        I = ElectromagneticWaves.intensity(E0)
        return I / C if absorbing else 2 * I / C


class RelativisticElectrodynamics:
    """Field-strength tensor and Lorentz force."""

    @staticmethod
    def field_tensor(Ex, Ey, Ez, Bx, By, Bz) -> np.ndarray:
        """Contravariant F^{mu nu} (mostly-minus convention, c=1)."""
        return np.array([
            [0,    -Ex, -Ey, -Ez],
            [Ex,    0, -Bz,  By],
            [Ey,   Bz,   0, -Bx],
            [Ez,  -By,  Bx,   0],
        ], dtype=float)

    @staticmethod
    def lorentz_force(q: float, v: np.ndarray, E: np.ndarray, B: np.ndarray) -> np.ndarray:
        return q * (E + np.cross(v, B))

    @staticmethod
    def invariants(Ex, Ey, Ez, Bx, By, Bz) -> tuple[float, float]:
        E2 = Ex ** 2 + Ey ** 2 + Ez ** 2
        B2 = Bx ** 2 + By ** 2 + Bz ** 2
        EB = Ex * Bx + Ey * By + Ez * Bz
        return E2 - B2, EB
