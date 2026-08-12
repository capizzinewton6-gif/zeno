"""Bravais lattice generators, Brillouin zones, and Fermi surfaces."""

from __future__ import annotations

import numpy as np

from physics.condensed_matter import CrystalLattice


class CondensedLattices:
    """Higher-level lattice utilities built on CrystalLattice."""

    crystal = CrystalLattice

    @staticmethod
    def brillouin_zone(real_lattice: np.ndarray, n: int = 50) -> dict:
        """Return reciprocal lattice and a sampling of the first BZ."""
        b = CrystalLattice.reciprocal(np.asarray(real_lattice, dtype=float))
        # sample within a cube in reciprocal space (qualitative)
        kx = np.linspace(-1, 1, n)
        ky = np.linspace(-1, 1, n)
        KX, KY = np.meshgrid(kx, ky)
        return {"reciprocal_lattice": b, "kx": kx, "ky": ky, "KX": KX, "KY": KY}

    @staticmethod
    def fermi_surface_2d(fermi_energy: float, band_dispersion, kx: np.ndarray, ky: np.ndarray) -> np.ndarray:
        KX, KY = np.meshgrid(kx, ky)
        E = band_dispersion(KX, KY)
        return np.isclose(E, fermi_energy, atol=0.05)

    @staticmethod
    def hexagonal_lattice(a: float) -> np.ndarray:
        """2D triangular/hexagonal Bravais lattice basis vectors."""
        return np.array([[a, 0.0], [a / 2, a * np.sqrt(3) / 2]])
