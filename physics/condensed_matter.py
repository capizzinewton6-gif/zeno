"""Band theory, crystal lattices, superconductivity, and phonons."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


KB = CONSTANTS.value("kB")
HBAR = CONSTANTS.value("hbar")


class CrystalLattice:
    """Bravais lattice generators and reciprocal lattice."""

    @staticmethod
    def cubic(a: float) -> np.ndarray:
        return a * np.eye(3)

    @staticmethod
    def fcc(a: float) -> np.ndarray:
        return a / 2 * np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=float)

    @staticmethod
    def bcc(a: float) -> np.ndarray:
        return a / 2 * np.array([[-1, 1, 1], [1, -1, 1], [1, 1, -1]], dtype=float)

    @staticmethod
    def reciprocal(real_lattice: np.ndarray) -> np.ndarray:
        a1, a2, a3 = real_lattice
        vol = np.dot(a1, np.cross(a2, a3))
        b1 = 2 * math.pi * np.cross(a2, a3) / vol
        b2 = 2 * math.pi * np.cross(a3, a1) / vol
        b3 = 2 * math.pi * np.cross(a1, a2) / vol
        return np.vstack([b1, b2, b3])


class BandTheory:
    """Tight-binding dispersion and effective mass."""

    @staticmethod
    def tight_binding_1d(k: np.ndarray, t: float = 1.0, a: float = 1.0) -> np.ndarray:
        """E(k) = -2t cos(k a) for a 1D nearest-neighbour chain."""
        return -2 * t * np.cos(k * a)

    @staticmethod
    def effective_mass_1d(k: float, t: float = 1.0, a: float = 1.0) -> float:
        """m* = hbar^2 / (d^2E/dk^2)."""
        d2E = 2 * t * a ** 2 * math.cos(k * a)
        return HBAR ** 2 / d2E if d2E != 0 else float("inf")

    @staticmethod
    def fermi_level_free_electron(n: float, m: float) -> float:
        """3D Fermi energy of a free electron gas with density n."""
        return (HBAR ** 2 / (2 * m)) * (3 * math.pi ** 2 * n) ** (2 / 3)


class Phonons:
    """Acoustic/optical phonon dispersion for a 1D diatomic chain."""

    @staticmethod
    def monatomic_dispersion(k: np.ndarray, C: float = 1.0, M: float = 1.0, a: float = 1.0) -> np.ndarray:
        """omega(k) = 2 sqrt(C/M) |sin(k a / 2)|."""
        return 2 * math.sqrt(C / M) * np.abs(np.sin(k * a / 2))

    @staticmethod
    def debye_model_density_of_states(omega: np.ndarray, omega_D: float) -> np.ndarray:
        """D(omega) ~ omega^2 up to Debye cutoff."""
        return np.where(omega < omega_D, 3 * omega ** 2 / omega_D ** 3, 0.0)


class Superconductivity:
    """BCS quantities and the London equations."""

    @staticmethod
    def bcs_gap(T: float, Tc: float, T0: float = 0.0) -> float:
        """Approximate BCS gap: Delta(0) = 1.764 kB Tc; vanishes near Tc as ~3.06 kB Tc sqrt(1-T/Tc)."""
        if T >= Tc:
            return 0.0
        if T <= T0:
            return 1.764 * KB * Tc
        return 3.06 * KB * Tc * math.sqrt(max(1 - T / Tc, 0.0))

    @staticmethod
    def coherence_length_xi0(vF: float, Tc: float) -> float:
        """BCS coherence length xi_0 = hbar vF / (pi Delta(0))."""
        return HBAR * vF / (math.pi * 1.764 * KB * Tc)

    @staticmethod
    def london_penetration_depth(n_s: float, m: float, e_charge: float) -> float:
        """lambda_L = sqrt(m / (mu0 n_s e^2))."""
        mu0 = CONSTANTS.value("mu0")
        return math.sqrt(m / (mu0 * n_s * e_charge ** 2))
