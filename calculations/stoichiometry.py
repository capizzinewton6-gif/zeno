"""Stoichiometry — moles, molarity, limiting reagents, and percent yields."""

import math


class Stoichiometry:
    """Stoichiometric calculations for chemical reactions."""

    AVOGADRO = 6.02214076e23  # mol^-1

    # --- Basic mole conversions ----------------------------------------
    @staticmethod
    def mass_to_moles(mass_g, molar_mass_g_mol):
        return mass_g / molar_mass_g_mol

    @staticmethod
    def moles_to_mass(moles, molar_mass_g_mol):
        return moles * molar_mass_g_mol

    @staticmethod
    def moles_to_molecules(moles):
        return moles * Stoichiometry.AVOGADRO

    @staticmethod
    def molecules_to_moles(molecules):
        return molecules / Stoichiometry.AVOGADRO

    # --- Molarity ------------------------------------------------------
    @staticmethod
    def molarity(moles, volume_L):
        return moles / volume_L

    @staticmethod
    def moles_from_molarity(molarity_M, volume_L):
        return molarity_M * volume_L

    @staticmethod
    def dilution(c1, v1, c2):
        """Compute V2 from dilution equation C1*V1 = C2*V2."""
        return (c1 * v1) / c2

    # --- Limiting reagent ----------------------------------------------
    @staticmethod
    def limiting_reagent(reactants):
        """reactants: list of dicts {name, moles, coefficient}.

        Returns the limiting reagent name and theoretical mole extent.
        """
        extents = []
        for r in reactants:
            coeff = r["coefficient"]
            if coeff <= 0:
                raise ValueError(f"Coefficient must be positive for {r['name']}")
            extents.append((r["name"], r["moles"] / coeff, r))
        limiting = min(extents, key=lambda x: x[1])
        return {
            "limiting_reagent": limiting[0],
            "extent_moles": limiting[1],
            "all_extents": [{"name": e[0], "extent": e[1]} for e in extents],
        }

    # --- Percent yield -------------------------------------------------
    @staticmethod
    def percent_yield(actual_mass_g, theoretical_mass_g):
        if theoretical_mass_g == 0:
            raise ValueError("Theoretical yield cannot be zero")
        return (actual_mass_g / theoretical_mass_g) * 100.0

    @staticmethod
    def theoretical_yield(limiting_moles, product_coefficient, product_molar_mass):
        return limiting_moles * product_coefficient * product_molar_mass

    # --- Percent composition / empirical formula -----------------------
    @staticmethod
    def percent_composition(masses, molar_masses):
        """masses: dict element->grams; molar_masses: dict element->g/mol."""
        moles = {el: masses[el] / molar_masses[el] for el in masses}
        total = sum(moles.values())
        ratios = {el: moles[el] / total for el in moles}
        min_mole = min(moles.values())
        empirical = {el: round(moles[el] / min_mole) for el in moles}
        return {"mole_ratios": ratios, "empirical_formula": empirical}

    @staticmethod
    def atom_economy(reactant_molar_masses, desired_product_mass, product_molar_mass):
        """Sheldon atom economy metric."""
        total_reactant_mass = sum(reactant_molar_masses)
        return (product_molar_mass / total_reactant_mass) * 100.0
