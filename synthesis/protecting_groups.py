"""Protecting groups — protection and deprotection strategy analysis."""


class ProtectingGroups:
    """Common protecting group strategies."""

    GROUPS = {
        "TBS (alcohol)": {"protects": "alcohol", "protect_reagent": "TBSCl, imidazole",
                          "deprotect": "TBAF or HF-pyridine", "stable_to": ["base", "mild acid", "hydrogenation"]},
        "Boc (amine)": {"protects": "amine", "protect_reagent": "Boc2O, base",
                        "deprotect": "TFA or HCl/dioxane", "stable_to": ["base", "hydrogenation"]},
        "Cbz (amine)": {"protects": "amine", "protect_reagent": "CbzCl, base",
                        "deprotect": "H2, Pd/C", "stable_to": ["acid", "base"]},
        "Fmoc (amine)": {"protects": "amine", "protect_reagent": "Fmoc-Cl",
                         "deprotect": "piperidine/DMF", "stable_to": ["acid"]},
        "Acetyl (alcohol/amine)": {"protects": "alcohol/amine", "protect_reagent": "Ac2O, pyridine",
                                   "deprotect": "K2CO3/MeOH or NH3/MeOH", "stable_to": ["mild acid", "hydrogenation"]},
        "MOM (alcohol)": {"protects": "alcohol", "protect_reagent": "MOMCl, base",
                          "deprotect": "acid (HCl)", "stable_to": ["base", "hydrogenation"]},
        "THP (alcohol)": {"protects": "alcohol", "protect_reagent": "DHP, PPTS",
                          "deprotect": "PPTS/EtOH or dilute acid", "stable_to": ["base", "organometallics"]},
    }

    def recommend(self, functional_group, conditions_to_survive=None):
        conditions_to_survive = conditions_to_survive or []
        candidates = []
        for name, info in self.GROUPS.items():
            if functional_group.lower() in info["protects"].lower():
                stable = all(c in info["stable_to"] for c in conditions_to_survive)
                candidates.append({
                    "protecting_group": name,
                    "protect_reagent": info["protect_reagent"],
                    "deprotect": info["deprotect"],
                    "stable_to": info["stable_to"],
                    "survives_conditions": stable,
                })
        return {"functional_group": functional_group,
                "conditions": conditions_to_survive,
                "recommendations": candidates}

    def list_groups(self):
        return list(self.GROUPS.keys())
