"""Hubble parameter evolution, redshift conversion, and distance measures."""

from __future__ import annotations

import numpy as np

from physics.astrophysics_cosmology import Cosmology


class CosmologyCalculator(Cosmology):
    """Extended cosmology distance/luminosity calculators."""

    def distance_modulus(self, z: float) -> float:
        """m - M = 5 log10(d_L / 10 pc)."""
        d_L = self.luminosity_distance(z)  # meters
        d_L_pc = d_L / 3.0856775814913673e16
        return 5 * np.log10(max(d_L_pc / 10, 1e-30))

    def lookback_time(self, z: float, n_steps: int = 2000) -> float:
        """t_L(z) = integral_0^z dz' / ((1+z') H(z'))."""
        zs = np.linspace(0, z, n_steps)
        Hz = np.array([self.hubble(zz) for zz in zs])
        integrand = 1.0 / ((1 + zs) * Hz)
        return float(np.trapz(integrand, zs))

    def hubble_diagram(self, z_array: np.ndarray) -> dict:
        d_L = np.array([self.luminosity_distance(z) for z in z_array])
        mu = np.array([self.distance_modulus(z) for z in z_array])
        return {"z": z_array.tolist(), "d_L_Mpc": (d_L / 3.0856775814913673e22).tolist(),
                "distance_modulus": mu.tolist()}

    @staticmethod
    def redshift_to_velocity(z: float) -> float:
        """Relativistic Doppler redshift -> recession velocity."""
        from tools.constant_engine import CONSTANTS
        c = CONSTANTS.value("c")
        beta = ((1 + z) ** 2 - 1) / ((1 + z) ** 2 + 1)
        return beta * c
