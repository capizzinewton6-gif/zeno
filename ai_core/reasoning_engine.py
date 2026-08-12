"""Reasoning engine — mechanistic, retrosynthetic, and thermochemical reasoning.

Delegates deep reasoning to the Gemini 2.5 Flash engine while providing
deterministic local scaffolds for common reasoning patterns so the UI
simulations remain functional offline.
"""

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_25_flash_engine import reason as gemini25_reason

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Mechanistic, retrosynthetic, and thermochemical reasoning."""

    def __init__(self, api_key=None):
        self.api_key = api_key

    # --- Local reasoning scaffolds -------------------------------------
    @staticmethod
    def mechanistic_scaffold(reaction):
        """Return a structured mechanism scaffold for a named reaction."""
        return {
            "reaction": reaction,
            "steps": [
                "1. Identify electrophile and nucleophile.",
                "2. Draw curved-arrow electron flow.",
                "3. Determine rate-determining step.",
                "4. Identify intermediates (carbocation, radical, etc.).",
                "5. Assess stereochemical outcome.",
                "6. Summarize overall transformation.",
            ],
        }

    @staticmethod
    def retrosynthetic_scaffold(target_smiles=None):
        """Return a retrosynthetic disconnection scaffold."""
        return {
            "target": target_smiles,
            "approach": [
                "Identify strategic bonds (C–C, C–heteroatom).",
                "Apply disconnection rules (FGA, FGI, C–C disconnection).",
                "Generate synthons and equivalent reagents.",
                "Evaluate precursor availability.",
                "Assemble forward route with protecting groups.",
            ],
        }

    @staticmethod
    def thermochemical_scaffold():
        """Return a thermochemical reasoning checklist."""
        return {
            "checks": [
                "Hess's Law cycle completeness",
                "Reference state consistency",
                "Phase-change contributions",
                "Heat capacity temperature dependence",
                "Entropy and Gibbs free energy sign analysis",
            ],
        }

    # --- Routed reasoning ----------------------------------------------
    def reason(self, prompt, context=None):
        local = {
            "mechanism_scaffold": self.mechanistic_scaffold(prompt),
            "retrosynthesis_scaffold": self.retrosynthetic_scaffold(),
            "thermochemistry_scaffold": self.thermochemical_scaffold(),
        }
        live = gemini25_reason(prompt, context, api_key=self.api_key)
        return {"local_scaffolds": local, "engine_response": live}
