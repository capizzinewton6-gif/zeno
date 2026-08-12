"""Thermodynamics — Hess's Law, van 't Hoff equation, and heat capacity."""

import math


class Thermodynamics:
    """Thermochemical calculations."""

    R = 8.314  # J/(mol*K)

    # --- Hess's Law ----------------------------------------------------
    @staticmethod
    def hess_law(delta_h_reactants, delta_h_products):
        """Sum of product formation enthalpies minus reactants."""
        return sum(delta_h_products) - sum(delta_h_reactants)

    @staticmethod
    def reaction_enthalpy(formation_enthalpies):
        """formation_enthalpies: dict {'reactants': {...}, 'products': {...}, 'coeffs': {...}}"""
        r = formation_enthalpies.get("reactants", {})
        p = formation_enthalpies.get("products", {})
        coeffs = formation_enthalpies.get("coeffs", {})
        dh = 0.0
        for sp, h in p.items():
            dh += h * coeffs.get(sp, 1)
        for sp, h in r.items():
            dh -= h * coeffs.get(sp, 1)
        return dh

    # --- Heat / calorimetry --------------------------------------------
    @staticmethod
    def heat_capacity(q_j, m_g, delta_t):
        """Specific heat capacity c = q / (m * dT)."""
        return q_j / (m_g * delta_t)

    @staticmethod
    def heat_transferred(m_g, specific_heat, delta_t):
        return m_g * specific_heat * delta_t

    @staticmethod
    def enthalpy_from_calorimetry(m_solution_g, c_solution, delta_t, moles_reacted):
        """q_rxn = -(m*c*dT); per mole = q_rxn / moles."""
        q = -(m_solution_g * c_solution * delta_t)
        return {"q_rxn_J": q, "dh_kJ_per_mol": (q / 1000.0) / moles_reacted if moles_reacted else None}

    # --- Gibbs free energy / entropy -----------------------------------
    @staticmethod
    def gibbs_free_energy(delta_h_kJ, delta_s_kJ_per_K, T_K):
        return delta_h_kJ - T_K * delta_s_kJ_per_K

    @staticmethod
    def gibbs_from_equilibrium(K, T_K):
        """dG = -RT ln(K)."""
        return -Thermodynamics.R * T_K * math.log(K) / 1000.0  # kJ/mol

    # --- van 't Hoff ---------------------------------------------------
    @staticmethod
    def van_t_hoff(K1, T1, T2, delta_h_J):
        """ln(K2/K1) = -dH/R * (1/T2 - 1/T1). Returns K2."""
        return K1 * math.exp((-delta_h_J / Thermodynamics.R) * (1.0 / T2 - 1.0 / T1))

    @staticmethod
    def van_t_hoff_slope(enthalpy_J):
        """Returns -dH/R for a van 't Hoff plot."""
        return -enthalpy_J / Thermodynamics.R
