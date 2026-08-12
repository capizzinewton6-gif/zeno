"""Heat transfer, statistical mechanics, kinetic theory, and phase transitions."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

from tools.constant_engine import CONSTANTS


KB = CONSTANTS.value("kB")
HBAR = CONSTANTS.value("hbar")


class HeatTransfer:
    """1D diffusion/heat equation solver on a finite-difference grid."""

    @staticmethod
    def solve_1d(length: float, alpha: float, T0: np.ndarray, t_final: float,
                 dt: float, dx: float, bc: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
        """Explicit FTCS scheme. T0 is the initial temperature profile."""
        nx = len(T0)
        n_steps = int(t_final / dt)
        T = T0.copy().astype(float)
        T[0], T[-1] = bc
        history = np.empty((n_steps + 1, nx))
        history[0] = T
        for n in range(1, n_steps + 1):
            Tn = T.copy()
            T[1:-1] = Tn[1:-1] + alpha * dt / dx ** 2 * (Tn[2:] - 2 * Tn[1:-1] + Tn[:-2])
            T[0], T[-1] = bc
            history[n] = T
        return history


class StatisticalMechanics:
    """Partition functions and distributions."""

    @staticmethod
    def boltzmann(energies: np.ndarray, T: float) -> np.ndarray:
        beta = 1.0 / (KB * T)
        weights = np.exp(-beta * energies)
        return weights / weights.sum()

    @staticmethod
    def partition_function(energies: np.ndarray, T: float) -> float:
        beta = 1.0 / (KB * T)
        return float(np.sum(np.exp(-beta * energies)))

    @staticmethod
    def free_energy(energies: np.ndarray, T: float) -> float:
        Z = StatisticalMechanics.partition_function(energies, T)
        return -KB * T * math.log(Z)

    @staticmethod
    def mean_energy(energies: np.ndarray, T: float) -> float:
        beta = 1.0 / (KB * T)
        weights = np.exp(-beta * energies)
        return float(np.sum(energies * weights) / np.sum(weights))

    @staticmethod
    def entropy(energies: np.ndarray, T: float) -> float:
        Z = StatisticalMechanics.partition_function(energies, T)
        U = StatisticalMechanics.mean_energy(energies, T)
        return (U / T) + KB * math.log(Z)


class QuantumStatistics:
    """Fermi-Dirac and Bose-Einstein distributions."""

    @staticmethod
    def fermi_dirac(energy: np.ndarray, mu: float, T: float) -> np.ndarray:
        beta = 1.0 / (KB * T)
        return 1.0 / (np.exp(beta * (energy - mu)) + 1.0)

    @staticmethod
    def bose_einstein(energy: np.ndarray, mu: float, T: float) -> np.ndarray:
        beta = 1.0 / (KB * T)
        return 1.0 / (np.exp(beta * (energy - mu)) - 1.0)

    @staticmethod
    def planck_spectrum(freq: np.ndarray, T: float) -> np.ndarray:
        """Spectral radiance (Planck) per unit frequency."""
        h = CONSTANTS.value("h")
        c = CONSTANTS.value("c")
        return (2 * h * freq ** 3 / c ** 2) / (np.exp(h * freq / (KB * T)) - 1.0)


class KineticTheory:
    """Maxwell-Boltzmann velocity distribution and derived quantities."""

    @staticmethod
    def maxwell_speed(speeds: np.ndarray, m: float, T: float) -> np.ndarray:
        f = np.sqrt(2 / math.pi) * (m / (KB * T)) ** 1.5 * speeds ** 2 * np.exp(-m * speeds ** 2 / (2 * KB * T))
        return f

    @staticmethod
    def mean_speed(m: float, T: float) -> float:
        return math.sqrt(8 * KB * T / (math.pi * m))

    @staticmethod
    def rms_speed(m: float, T: float) -> float:
        return math.sqrt(3 * KB * T / m)

    @staticmethod
    def mean_free_path(diameter: float, n_density: float) -> float:
        return 1.0 / (math.sqrt(2) * math.pi * diameter ** 2 * n_density)


@dataclass
class PhaseTransition:
    name: str
    critical_temp: float
    order: int
    description: str


PHASE_TRANSITIONS = [
    PhaseTransition("superconducting (conventional)", 9.2, 2, "BCS pairing, e.g. Nb"),
    PhaseTransition("Curie (ferromagnetic)", 1043.0, 2, "Iron"),
    PhaseTransition("lambda (He-4)", 2.17, 2, "Superfluid transition"),
    PhaseTransition("water boiling", 373.15, 1, "Liquid-gas (latent heat)"),
]
