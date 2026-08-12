"""Retrosynthesis engine — disconnection approach and precursor planning."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_25_flash_engine import reason as gemini25_reason


class RetrosynthesisEngine:
    """Apply retrosynthetic disconnection logic to a target molecule."""

    DISCONNECTION_RULES = [
        {"bond": "C-O (ester)", "transform": "Fischer esterification (acid + alcohol)"},
        {"bond": "C-N (amide)", "transform": "Amide coupling (carboxylic acid + amine)"},
        {"bond": "C=C (alkene)", "transform": "Wittig olefination or aldol condensation"},
        {"bond": "biaryl C-C", "transform": "Suzuki / Negishi / Stille coupling"},
        {"bond": "C-OH (alcohol)", "transform": "Grignard addition to carbonyl"},
        {"bond": "C-X reduction", "transform": "Hydrogenolysis or reduction"},
    ]

    def __init__(self, api_key=None):
        self.api_key = api_key

    def disconnect(self, target_smiles, max_depth=3):
        """Return a retrosynthetic route scaffold."""
        route = {
            "target": target_smiles,
            "max_depth": max_depth,
            "disconnects": [],
        }
        for rule in self.DISCONNECTION_RULES[:max_depth]:
            route["disconnects"].append({
                "bond": rule["bond"],
                "transform": rule["transform"],
                "precursors": ["[precursor A]", "[precursor B]"],
            })
        route["engine_note"] = "Scaffold generated locally; configure GEMINI_API_KEY for AI-driven route scoring."
        # Optionally enrich with Gemini reasoning (offline-safe)
        enriched = gemini25_reason(
            f"Propose a retrosynthetic disconnection strategy for: {target_smiles}",
            context={"target": target_smiles}, api_key=self.api_key
        )
        route["ai_enrichment"] = enriched
        return route

    def list_rules(self):
        return self.DISCONNECTION_RULES
