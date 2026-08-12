"""Harmonic oscillators, finite wells, and 1D wave propagation."""

from __future__ import annotations

import numpy as np

from physics.classical_mechanics import HarmonicOscillator
from physics.quantum_mechanics import InfiniteSquareWell
from calculations.field_solvers import FieldSolvers


class Potentials1D:
    """Common 1D potentials and their analytical/numerical tools."""

    @staticmethod
    def harmonic(x: np.ndarray, k: float = 1.0) -> np.ndarray:
        return 0.5 * k * x ** 2

    @staticmethod
    def finite_well(x: np.ndarray, V0: float = 10.0, a: float = 1.0) -> np.ndarray:
        return np.where(np.abs(x) < a, -V0, 0.0)

    @staticmethod
    def barrier(x: np.ndarray, V0: float = 5.0, a: float = 0.5) -> np.ndarray:
        return np.where(np.abs(x) < a, V0, 0.0)

    @staticmethod
    def wave_propagation(u0: np.ndarray, ut0: np.ndarray, c: float, dx: float, dt: float, n_steps: int) -> np.ndarray:
        return FieldSolvers.wave_1d(u0, ut0, c, dx, dt, n_steps)
