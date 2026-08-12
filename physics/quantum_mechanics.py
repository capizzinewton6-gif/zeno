"""Wavefunctions, operators, spin, perturbation theory, and tunneling."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


HBAR = CONSTANTS.value("hbar")
ME = CONSTANTS.value("me")
E = CONSTANTS.value("e")


class InfiniteSquareWell:
    """Particle in a 1D box of width L, hard walls at 0 and L."""

    def __init__(self, L: float = 1.0, m: float = ME):
        self.L = L
        self.m = m

    def energy(self, n: int) -> float:
        return (n ** 2 * math.pi ** 2 * HBAR ** 2) / (2 * self.m * self.L ** 2)

    def energy_levels(self, n_max: int) -> np.ndarray:
        return np.array([self.energy(n) for n in range(1, n_max + 1)])

    def wavefunction(self, n: int, x: np.ndarray) -> np.ndarray:
        return np.sqrt(2 / self.L) * np.sin(n * math.pi * x / self.L)

    def probability_density(self, n: int, x: np.ndarray) -> np.ndarray:
        psi = self.wavefunction(n, x)
        return np.abs(psi) ** 2


class HarmonicOscillatorQuantum:
    """1D quantum harmonic oscillator: Hermite-Gauss eigenstates."""

    def __init__(self, m: float = ME, omega: float = 1.0):
        self.m = m
        self.omega = omega
        self.alpha = self.m * omega / HBAR

    def energy(self, n: int) -> float:
        return HBAR * self.omega * (n + 0.5)

    def wavefunction(self, n: int, x: np.ndarray) -> np.ndarray:
        xi = np.sqrt(self.alpha) * x
        norm = (self.alpha / math.pi) ** 0.25 / np.sqrt(2 ** n * math.factorial(n))
        Hn = np.polynomial.hermite.Hermite([0] * n + [1])(xi)
        return norm * Hn * np.exp(-xi ** 2 / 2)

    def probability_density(self, n: int, x: np.ndarray) -> np.ndarray:
        return np.abs(self.wavefunction(n, x)) ** 2

    @staticmethod
    def ladder_operators():
        """Symbolic a, a-dagger in terms of x and p."""
        x, p, m, omega, hbar = sp.symbols("x p m omega hbar", positive=True)
        a = sp.sqrt(m * omega / (2 * hbar)) * (x + sp.I * p / (m * omega))
        ad = sp.sqrt(m * omega / (2 * hbar)) * (x - sp.I * p / (m * omega))
        return a, ad


@dataclass
class TunnelingResult:
    transmission: float
    reflection: float
    energy: float
    barrier_height: float
    barrier_width: float


class QuantumTunneling:
    """Rectangular barrier tunneling (WKB / exact square-barrier)."""

    @staticmethod
    def rectangular_barrier(E: float, V0: float, a: float, m: float = ME) -> TunnelingResult:
        """Transmission through a square barrier of height V0, width a."""
        if E >= V0:
            k = math.sqrt(2 * m * (E - V0)) / HBAR
            T = 1.0 / (1.0 + ((V0 ** 2 * np.sinh(0) ** 2)) / (4 * E * (E - V0)))  # placeholder branch
            # For E > V0 the formula uses sin:
            T = 1.0 / (1.0 + (V0 ** 2 * np.sin(k * a) ** 2) / (4 * E * (E - V0)))
        else:
            kappa = math.sqrt(2 * m * (V0 - E)) / HBAR
            T = 1.0 / (1.0 + (V0 ** 2 * np.sinh(kappa * a) ** 2) / (4 * E * (V0 - E)))
        return TunnelingResult(transmission=float(T), reflection=float(1 - T), energy=E,
                               barrier_height=V0, barrier_width=a)

    @staticmethod
    def wkb_alpha(E: float, m: float, mass_energy_distance: float) -> float:
        """WKB decay constant for a barrier (mass_energy_distance=2m(V-E)/hbar^2)."""
        return math.sqrt(max(mass_energy_distance, 0.0))


class SpinOperators:
    """Pauli matrices and spin-(1/2) algebra."""

    SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
    SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)

    @classmethod
    def s_squared(cls) -> np.ndarray:
        """S^2 for spin-1/2: (3/4) hbar^2 I."""
        return 0.75 * HBAR ** 2 * np.eye(2)

    @classmethod
    def rotation(cls, axis: str, theta: float) -> np.ndarray:
        """Spin-1/2 rotation operator exp(-i theta sigma_axis / 2)."""
        S = {"x": cls.SIGMA_X, "y": cls.SIGMA_Y, "z": cls.SIGMA_Z}[axis]
        return (np.eye(2) * np.cos(theta / 2) - 1j * S * np.sin(theta / 2))


class PerturbationTheory:
    """Time-independent perturbation theory for non-degenerate levels."""

    @staticmethod
    def first_order_energy(pert_matrix: np.ndarray, n: int) -> float:
        """E_n^(1) = <n|V|n>."""
        return float(np.real(pert_matrix[n, n]))

    @staticmethod
    def second_order_energy(energies: np.ndarray, pert_matrix: np.ndarray, n: int) -> float:
        """E_n^(2) = sum_{m != n} |<m|V|n>|^2 / (E_n - E_m)."""
        total = 0.0
        for m in range(len(energies)):
            if m == n:
                continue
            denom = energies[n] - energies[m]
            if abs(denom) < 1e-15:
                continue
            total += abs(pert_matrix[m, n]) ** 2 / denom
        return float(total)
