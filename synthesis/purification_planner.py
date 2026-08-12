"""Purification planner — column chromatography, recrystallization, distillation SOPs."""


class PurificationPlanner:
    """Generate purification SOPs."""

    def column_chromatography(self, sample_mass_g, n_components=2, polarity="medium"):
        """Recommend silica loading and solvent system."""
        silica = sample_mass_g * 50  # 50:1 silica:sample
        systems = {
            "low": "hexanes/EtOAc 95:5",
            "medium": "hexanes/EtOAc 80:20",
            "high": "DCM/MeOH 90:10",
        }
        return {
            "method": "flash column chromatography",
            "silica_mass_g": round(silica, 1),
            "column_diameter_cm": round((sample_mass_g / 5) ** 0.5 + 1, 1),
            "solvent_system": systems.get(polarity, systems["medium"]),
            "gradient": "step gradient recommended",
            "n_components": n_components,
            "SOP": [
                "1. Pack silica slurry in chosen solvent.",
                "2. Load sample pre-adsorbed on silica.",
                "3. Elute with gradient, collect fractions.",
                "4. Analyze by TLC, combine pure fractions.",
                "5. Evaporate solvent under reduced pressure.",
            ],
        }

    def recrystallization(self, compound_name, solvent_options=None):
        solvent_options = solvent_options or ["ethanol/water", "hexanes/ethyl acetate", "toluene"]
        return {
            "method": "recrystallization",
            "compound": compound_name,
            "solvent_options": solvent_options,
            "SOP": [
                "1. Dissolve in minimum hot solvent.",
                "2. Filter hot to remove insolubles.",
                "3. Cool slowly to crystallize.",
                "4. Chill in ice bath.",
                "5. Filter crystals, wash with cold solvent, dry.",
            ],
        }

    def distillation(self, bp_target_C, bp_impurity_C=None):
        feasible = bp_impurity_C is None or abs(bp_target_C - bp_impurity_C) > 20
        return {
            "method": "fractional distillation" if not feasible else "simple distillation",
            "target_bp_C": bp_target_C,
            "feasible": feasible,
            "SOP": [
                "1. Charge still with crude mixture.",
                "2. Heat gradually with stirring.",
                "3. Collect fraction at target boiling point.",
                "4. Monitor head temperature; switch receivers as needed.",
                "5. Store distilled product under inert atmosphere if sensitive.",
            ],
        }
