"""Quantum math — Schrodinger equation matrix elements and basis sets."""

import math


class QuantumMath:
    """Basic quantum-mechanical helpers for electronic structure."""

    HBAR = 1.054571817e-34  # J*s
    ME = 9.1093837015e-31   # kg
    E0 = 8.8541878128e-12   # F/m
    E_CHARGE = 1.602176634e-19  # C
    A0 = 5.29177210903e-11  # Bohr radius (m)
    HARTREE = 4.3597447222071e-18  # J

    # --- Particle in a box --------------------------------------------
    @staticmethod
    def particle_in_box_energy(n, length_m, mass_kg=None):
        """E_n = n^2 h^2 / (8 m L^2)."""
        if mass_kg is None:
            mass_kg = QuantumMath.ME
        h = 2 * math.pi * QuantumMath.HBAR
        return (n ** 2 * h ** 2) / (8 * mass_kg * length_m ** 2)

    # --- Harmonic oscillator ------------------------------------------
    @staticmethod
    def harmonic_oscillator_energy(n, omega):
        """E_n = (n + 1/2) hbar omega."""
        return (n + 0.5) * QuantumMath.HBAR * omega

    @staticmethod
    def force_constant_frequency(k, mass_kg):
        """omega = sqrt(k/m)."""
        return math.sqrt(k / mass_kg)

    # --- Hydrogen atom -------------------------------------------------
    @staticmethod
    def hydrogen_energy_n(n):
        """E_n = -13.6 / n^2 eV (Rydberg approximation)."""
        return -13.6 / (n ** 2)

    @staticmethod
    def bohr_radius_n(n, z=1):
        """Bohr orbit radius: r_n = n^2 a0 / Z."""
        return (n ** 2) * QuantumMath.A0 / z

    # --- Basis set overlaps (STO-1G Gaussian approximation) ------------
    @staticmethod
    def gaussian_overlap(alpha, beta, R):
        """Overlap of two s-type Gaussians separated by R (bohr)."""
        prefactor = ((2 * alpha / math.pi) ** 0.75) * ((2 * beta / math.pi) ** 0.75)
        gamma = alpha + beta
        K = prefactor * (math.pi / gamma) ** 1.5 * math.exp(-alpha * beta / gamma * R ** 2)
        return K

    # --- Unit conversions ---------------------------------------------
    @staticmethod
    def ev_to_joules(ev):
        return ev * QuantumMath.E_CHARGE

    @staticmethod
    def hartree_to_ev(hartree):
        return hartree * 27.2114

    @staticmethod
    def joules_to_hartree(joules):
        return joules / QuantumMath.HARTREE
