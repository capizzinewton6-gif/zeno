"""Equilibrium — Ka, Kb, Ksp, pH, and buffer capacity calculations."""

import math


class Equilibrium:
    """Acid-base and solubility equilibrium calculations."""

    KW_25C = 1.0e-14  # water autoionization at 25 C

    # --- pH basics -----------------------------------------------------
    @staticmethod
    def ph_from_h(h_conc):
        return -math.log10(h_conc)

    @staticmethod
    def h_from_ph(ph):
        return 10 ** (-ph)

    @staticmethod
    def poh_from_oh(oh_conc):
        return -math.log10(oh_conc)

    # --- Ka / Kb -------------------------------------------------------
    @staticmethod
    def ka_from_kb(kb):
        return Equilibrium.KW_25C / kb

    @staticmethod
    def kb_from_ka(ka):
        return Equilibrium.KW_25C / ka

    @staticmethod
    def pka_from_ka(ka):
        return -math.log10(ka)

    @staticmethod
    def ka_from_pka(pka):
        return 10 ** (-pka)

    # --- Weak acid/base pH --------------------------------------------
    @staticmethod
    def weak_acid_ph(ka, concentration_M):
        """Approximate [H+] = sqrt(Ka * C) for weak acid."""
        h = math.sqrt(ka * concentration_M)
        return Equilibrium.ph_from_h(h)

    @staticmethod
    def weak_base_ph(kb, concentration_M):
        oh = math.sqrt(kb * concentration_M)
        pOH = Equilibrium.poh_from_oh(oh)
        return 14.0 - pOH

    # --- Buffers (Henderson-Hasselbalch) ------------------------------
    @staticmethod
    def henderson_hasselbalch(pka, base_conc, acid_conc):
        return pka + math.log10(base_conc / acid_conc)

    @staticmethod
    def buffer_capacity(acid_conc, base_conc, ka, h=1e-7):
        """Van Slyke buffer capacity (approximate)."""
        return 2.303 * (acid_conc * ka * h) / ((ka + h) ** 2) + 2.303 * base_conc * 1e-7

    # --- Ksp / solubility ---------------------------------------------
    @staticmethod
    def molar_solubility_from_ksp(ksp, ion_stoichiometries):
        """ion_stoichiometries: list of stoichiometric coefficients."""
        n = sum(ion_stoichiometries)
        product = 1.0
        for coeff in ion_stoichiometries:
            product *= coeff ** coeff
        return (ksp / product) ** (1.0 / n)

    @staticmethod
    def ksp_from_solubility(s, ion_stoichiometries):
        product = 1.0
        for coeff in ion_stoichiometries:
            product *= (coeff * s) ** coeff
        return product

    # --- Common ion effect --------------------------------------------
    @staticmethod
    def common_ion_solubility(ksp, coeff_anion, coeff_cation, common_ion_conc):
        """Solubility in presence of a common ion (simplified for 1:1 salts)."""
        if coeff_anion == 1 and coeff_cation == 1:
            return ksp / common_ion_conc
        return (ksp / common_ion_conc) ** (1.0 / (coeff_anion + coeff_cation - 1))
