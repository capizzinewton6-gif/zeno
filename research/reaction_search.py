"""Reaction search — search reaction databases for transformations."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_15_flash_engine import process as gemini15_process


class ReactionSearch:
    """Search reaction knowledge bases (local + AI-assisted)."""

    NAME_REACTIONS = {
        "Suzuki": {"type": "Pd-catalyzed cross-coupling", "reactants": "aryl halide + boronic acid",
                   "products": "biaryl", "reference": "Suzuki, A. Pure Appl. Chem. 1985, 57, 1749."},
        "Heck": {"type": "Pd-catalyzed coupling", "reactants": "aryl halide + alkene",
                 "products": "substituted alkene", "reference": "Heck, R.F. JACS 1968, 90, 5518."},
        "Sonogashira": {"type": "Pd/Cu-catalyzed coupling", "reactants": "aryl halide + terminal alkyne",
                        "products": "aryl alkyne", "reference": "Sonogashira et al. TL 1975, 4467."},
        "Buchwald-Hartwig": {"type": "Pd-catalyzed amination", "reactants": "aryl halide + amine",
                             "products": "aryl amine", "reference": "Buchwald, Hartwig reviews."},
        "Grignard": {"type": "organometallic addition", "reactants": "RMgX + carbonyl",
                     "products": "alcohol", "reference": "Grignard, V. CR Acad. Sci. 1900."},
        "Diels-Alder": {"type": "[4+2] cycloaddition", "reactants": "diene + dienophile",
                        "products": "cyclohexene", "reference": "Diels, O.; Alder, K. 1928."},
    }

    def __init__(self, api_key=None):
        self.api_key = api_key

    def search_by_name(self, name):
        return self.NAME_REACTIONS.get(name, {"error": f"Reaction '{name}' not in local database"})

    def search_by_functional_group(self, fg):
        results = []
        for name, info in self.NAME_REACTIONS.items():
            if fg.lower() in info["reactants"].lower() or fg.lower() in info["products"].lower():
                results.append({"name": name, **info})
        return {"functional_group": fg, "matches": results}

    def ai_search(self, query):
        """Use Gemini 1.5 Flash for fast reaction literature preprocessing."""
        return gemini15_process(f"Find named reactions matching: {query}", context={"module": "reaction_search"},
                                api_key=self.api_key)

    def list_reactions(self):
        return list(self.NAME_REACTIONS.keys())
