"""Reaction planner — reagents, solvents, catalyst selection, order of addition."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gemini_25_flash_engine import reason as gemini25_reason


class ReactionPlanner:
    """Plan reagents, solvents, catalysts, and addition order."""

    SOLVENT_PROPERTIES = {
        "DCM": {"bp_C": 40, "polarity": "low", "inert": True},
        "THF": {"bp_C": 66, "polarity": "medium", "inert": True},
        "DMF": {"bp_C": 153, "polarity": "high", "inert": False},
        "toluene": {"bp_C": 111, "polarity": "low", "inert": True},
        "water": {"bp_C": 100, "polarity": "high", "inert": False},
        "ethanol": {"bp_C": 78, "polarity": "medium", "inert": False},
        "acetonitrile": {"bp_C": 82, "polarity": "medium", "inert": True},
    }

    def __init__(self, api_key=None):
        self.api_key = api_key

    def plan(self, reaction_type, target=None, reactants=None):
        plan = {
            "reaction_type": reaction_type,
            "reagents": self._reagents(reaction_type),
            "solvents": self._solvents(reaction_type),
            "catalyst": self._catalyst(reaction_type),
            "addition_order": self._addition_order(reaction_type),
            "conditions": {"temperature_C": self._temperature(reaction_type), "atmosphere": self._atmosphere(reaction_type)},
        }
        enriched = gemini25_reason(
            f"Detail a reaction plan for a {reaction_type} synthesis.",
            context={"target": target, "reactants": reactants}, api_key=self.api_key
        )
        plan["ai_enrichment"] = enriched
        return plan

    def _reagents(self, rt):
        return {
            "Suzuki": ["boronic acid", "aryl halide", "base (K2CO3)"],
            "Grignard": ["Mg turnings", "alkyl/aryl halide", "carbonyl substrate"],
            "esterification": ["carboxylic acid", "alcohol", "acid catalyst (H2SO4)"],
            "amide_coupling": ["carboxylic acid", "amine", "coupling reagent (EDC/HATU)"],
            "hydrogenation": ["H2 gas", "Pd/C catalyst"],
        }.get(rt, ["[specify reagents]"])

    def _solvents(self, rt):
        return {
            "Suzuki": ["THF/water", "dioxane/water"],
            "Grignard": ["anhydrous THF", "diethyl ether"],
            "esterification": ["toluene", "neat"],
            "amide_coupling": ["DMF", "DCM"],
            "hydrogenation": ["ethanol", "ethyl acetate"],
        }.get(rt, ["[specify solvent]"])

    def _catalyst(self, rt):
        return {
            "Suzuki": "Pd(PPh3)4", "Grignard": None,
            "esterification": "H2SO4 (acid)", "amide_coupling": "HATU/EDC",
            "hydrogenation": "Pd/C",
        }.get(rt, None)

    def _addition_order(self, rt):
        return {
            "Suzuki": ["1. aryl halide + boronic acid", "2. Pd catalyst", "3. base, heat"],
            "Grignard": ["1. Mg in THF", "2. add halide slowly", "3. add carbonyl at 0 C"],
            "esterification": ["1. acid + alcohol", "2. catalytic H2SO4", "3. reflux, remove water"],
            "amide_coupling": ["1. acid + base", "2. coupling reagent", "3. add amine"],
            "hydrogenation": ["1. substrate + catalyst", "2. purge with N2 then H2", "3. stir under H2"],
        }.get(rt, ["1. combine reactants", "2. add reagent", "3. heat/stir"])

    def _temperature(self, rt):
        return {"Suzuki": 80, "Grignard": 0, "esterification": 80,
                "amide_coupling": 25, "hydrogenation": 25}.get(rt, 25)

    def _atmosphere(self, rt):
        return {"Grignard": "N2/Ar", "hydrogenation": "H2",
                "Suzuki": "N2", "esterification": "air"}.get(rt, "air")
