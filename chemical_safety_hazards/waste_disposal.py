"""Waste disposal — solvent segregation, heavy metal precipitation, neutralization."""


class WasteDisposal:
    """Recommend waste handling procedures."""

    SOLVENT_STREAMS = {
        "halogenated": ["dichloromethane", "chloroform", "carbon tetrachloride", "1,2-dichloroethane"],
        "non_halogenated": ["ethanol", "acetone", "hexanes", "ethyl acetate", "toluene", "THF"],
        "aqueous_acidic": ["dilute acid waste"],
        "aqueous_basic": ["dilute base waste"],
        "heavy_metal": ["solutions containing Cr, Pb, Hg, Cd, Ag"],
        "oil": ["vacuum pump oil", "mineral oil"],
    }

    def segregate_solvent(self, solvent):
        cl = solvent.lower()
        for stream, members in self.SOLVENT_STREAMS.items():
            for m in members:
                if m in cl:
                    return {"solvent": solvent, "stream": stream}
        return {"solvent": solvent, "stream": "non_halogenated", "note": "default; verify locally"}

    def neutralize_acid(self, acid_pH, target_pH=7, base_normality=1.0, volume_L=1.0):
        """Estimate base volume to neutralize acid (simplified, 1:1)."""
        import math
        h_initial = 10 ** (-acid_pH)
        h_target = 10 ** (-target_pH)
        moles_H = (h_initial - h_target) * volume_L
        base_volume_L = moles_H / base_normality
        return {"base_volume_L": round(base_volume_L, 4), "base_normality": base_normality,
                "note": "Add base slowly with stirring and monitor pH."}

    def precipitate_heavy_metal(self, metal, concentration_mg_L, volume_L):
        """Recommend precipitation reagent for common heavy metals."""
        reagents = {
            "Cr": "reduce Cr(VI) to Cr(III) with bisulfite, then precipitate as hydroxide (pH ~8)",
            "Pb": "precipitate as carbonate or hydroxide (pH ~8-9)",
            "Hg": "precipitate as sulfide (Na2S); handle with extreme caution",
            "Cd": "precipitate as hydroxide (pH > 10)",
            "Ag": "precipitate as chloride (NaCl)",
        }
        mass_mg = concentration_mg_L * volume_L
        return {"metal": metal, "reagent": reagents.get(metal, "consult local EHS"),
                "mass_mg": round(mass_mg, 2),
                "note": "Filter precipitate; dispose as hazardous solid per regulations."}

    def list_streams(self):
        return list(self.SOLVENT_STREAMS.keys())
