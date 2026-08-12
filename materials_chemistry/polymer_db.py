"""Polymer database — Mn, Mw, PDI, and glass transition temperature (Tg)."""

import statistics


class PolymerDB:
    """Polymer molecular-weight distribution and thermal properties."""

    POLYMERS = {
        "PMMA": {"Tg_C": 105, "Tm_C": None, "solvent": "THF"},
        "polystyrene": {"Tg_C": 100, "Tm_C": None, "solvent": "THF"},
        "PET": {"Tg_C": 75, "Tm_C": 260, "solvent": "HFIP"},
        "nylon-6,6": {"Tg_C": 50, "Tm_C": 265, "solvent": "formic acid"},
        "PE": {"Tg_C": -125, "Tm_C": 130, "solvent": "decahydronaphthalene (hot)"},
        "PP": {"Tg_C": -10, "Tm_C": 165, "solvent": "decahydronaphthalene (hot)"},
        "PCL": {"Tg_C": -60, "Tm_C": 60, "solvent": "chloroform"},
    }

    @staticmethod
    def molecular_weight_distribution(masses, intensities):
        """Compute Mn, Mw, PDI from GPC distribution."""
        total_i = sum(intensities)
        if total_i == 0:
            return {"Mn": 0, "Mw": 0, "PDI": 0}
        Mn = sum(m * i for m, i in zip(masses, intensities)) / total_i
        Mw = sum(m ** 2 * i for m, i in zip(masses, intensities)) / sum(m * i for m, i in zip(masses, intensities))
        return {"Mn": round(Mn), "Mw": round(Mw), "PDI": round(Mw / Mn, 3)}

    def lookup(self, name):
        return self.POLYMERS.get(name.lower(), None)

    def list_polymers(self):
        return list(self.POLYMERS.keys())
