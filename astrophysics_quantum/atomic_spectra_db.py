"""NIST-style atomic energy levels, transition probabilities, quantum numbers."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class AtomicLevel:
    element: str
    n: int
    L: str
    J: float
    energy_eV: float


@dataclass
class Transition:
    element: str
    lower: AtomicLevel
    upper: AtomicLevel
    wavelength_nm: float
    A: float  # Einstein A coefficient (1/s)


class AtomicSpectraDB:
    """A small built-in atomic-energy-level database (hydrogen Balmer series)."""

    @staticmethod
    def hydrogen_level(n: int) -> float:
        """Bohr-model energy: E_n = -13.6 eV / n^2."""
        return -13.6 / n ** 2

    @staticmethod
    def balmer_series(n_upper_max: int = 7) -> list[Transition]:
        R_inf = 1.0973731568e7  # 1/m
        transitions: list[Transition] = []
        for n in range(3, n_upper_max + 1):
            inv_lambda = R_inf * (1 / 4 - 1 / n ** 2)
            wl = 1e9 / inv_lambda  # nm
            lower = AtomicLevel("H", 2, "S", 0.5, AtomicSpectraDB.hydrogen_level(2))
            upper = AtomicLevel("H", n, "P", 0.5, AtomicSpectraDB.hydrogen_level(n))
            transitions.append(Transition("H", lower, upper, wl, A=1e7 / n ** 3))
        return transitions

    @staticmethod
    def rydberg_formula(n1: int, n2: int, Z: int = 1) -> float:
        R_inf = 1.0973731568e7
        return 1e9 / (R_inf * Z ** 2 * (1 / n1 ** 2 - 1 / n2 ** 2))  # nm
