"""Electrochemistry — Nernst equation, standard reduction potentials, Faraday's laws."""

import math


class Electrochemistry:
    """Electrochemical calculations."""

    R = 8.314   # J/(mol*K)
    F = 96485.33212  # C/mol
    NERNST_CONST_25C = 0.025693  # V (RT/F at 25 C)

    # --- Cell potential ------------------------------------------------
    @staticmethod
    def cell_potential(E_cathode, E_anode):
        return E_cathode - E_anode

    @staticmethod
    def nernst(E0, n_electrons, reaction_quotient_Q, T_K=298.15):
        """E = E0 - (RT/nF) ln Q."""
        return E0 - (Electrochemistry.R * T_K / (n_electrons * Electrochemistry.F)) * math.log(reaction_quotient_Q)

    @staticmethod
    def nernst_25c(E0, n_electrons, Q):
        """Nernst equation at 25 C using log10: E = E0 - (0.05916/n) log Q."""
        return E0 - (0.05916 / n_electrons) * math.log10(Q)

    # --- Gibbs from cell potential ------------------------------------
    @staticmethod
    def gibbs_from_potential(E_cell, n_electrons):
        """dG = -nFE."""
        return -n_electrons * Electrochemistry.F * E_cell  # J/mol

    @staticmethod
    def equilibrium_constant(E0, n_electrons, T_K=298.15):
        """ln K = nFE0 / RT."""
        return math.exp(n_electrons * Electrochemistry.F * E0 / (Electrochemistry.R * T_K))

    # --- Faraday's laws ------------------------------------------------
    @staticmethod
    def mass_deposited(current_A, time_s, molar_mass, n_electrons):
        """m = (I * t * M) / (n * F)."""
        return (current_A * time_s * molar_mass) / (n_electrons * Electrochemistry.F)

    @staticmethod
    def moles_electrons(current_A, time_s):
        return (current_A * time_s) / Electrochemistry.F

    @staticmethod
    def time_for_mass(mass_g, current_A, molar_mass, n_electrons):
        return (mass_g * n_electrons * Electrochemistry.F) / (current_A * molar_mass)
