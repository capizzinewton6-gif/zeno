"""Partition functions and Fermi-Dirac/Bose-Einstein distributions."""

from __future__ import annotations

import math

import numpy as np

from tools.constant_engine import CONSTANTS
from physics.thermodynamics import StatisticalMechanics, QuantumStatistics


KB = CONSTANTS.value("kB")


class StatisticalPhysics:
    """Convenience aggregator over the thermodynamics statistical machinery."""

    partition_function = staticmethod(StatisticalMechanics.partition_function)
    free_energy = staticmethod(StatisticalMechanics.free_energy)
    mean_energy = staticmethod(StatisticalMechanics.mean_energy)
    entropy = staticmethod(StatisticalMechanics.entropy)
    boltzmann = staticmethod(StatisticalMechanics.boltzmann)
    fermi_dirac = staticmethod(QuantumStatistics.fermi_dirac)
    bose_einstein = staticmethod(QuantumStatistics.bose_einstein)
    planck_spectrum = staticmethod(QuantumStatistics.planck_spectrum)

    @staticmethod
    def heat_capacity_from_spectrum(energies: np.ndarray, T_range: np.ndarray) -> np.ndarray:
        """C(T) = d<U>/dT for a discrete spectrum."""
        U = np.array([StatisticalMechanics.mean_energy(energies, T) for T in T_range])
        return np.gradient(U, T_range)

    @staticmethod
    def stefan_boltzmann_flux(T: float) -> float:
        sigma = CONSTANTS.value("sigma")
        return sigma * T ** 4
