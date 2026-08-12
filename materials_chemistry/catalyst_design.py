"""Catalyst design — active site geometry, TOF, and adsorption energy."""


class CatalystDesign:
    """Heterogeneous and homogeneous catalyst descriptors."""

    @staticmethod
    def turnover_frequency(moles_product, moles_active_site, time_s):
        """TOF = (mol product) / (mol active site * time)."""
        return moles_product / (moles_active_site * time_s)

    @staticmethod
    def turnover_number(moles_product, moles_active_site):
        return moles_product / moles_active_site

    @staticmethod
    def sabatier_volcano(adsorption_energy_kJ_mol):
        """Volcano plot heuristic: optimal E_ads ~ -1.5 eV (~ -145 kJ/mol)."""
        optimal = -145.0
        if adsorption_energy_kJ_mol > optimal:
            return {"regime": "under-binding", "note": "Weak adsorption; reactants do not activate."}
        if adsorption_energy_kJ_mol < optimal:
            return {"regime": "over-binding", "note": "Strong adsorption; products do not desorb."}
        return {"regime": "optimal", "note": "Near Sabatier optimum."}

    @staticmethod
    def arrhenius_to_activity(A, Ea_kJ_mol, T_K):
        import math
        R = 8.314e-3  # kJ/mol/K
        return A * math.exp(-Ea_kJ_mol / (R * T_K))

    ACTIVE_SITE_MOTIFS = {
        "square_planar_Pd": {"coordination": 4, "typical_rxn": "cross-coupling"},
        "octahedral_Ru": {"coordination": 6, "typical_rxn": "olefin metathesis"},
        "tetrahedral_Zn": {"coordination": 4, "typical_rxn": "hydrolysis"},
        "single_atom_M_N4": {"coordination": 4, "typical_rxn": "ORR/CO2 reduction"},
    }

    def motifs(self):
        return self.ACTIVE_SITE_MOTIFS
