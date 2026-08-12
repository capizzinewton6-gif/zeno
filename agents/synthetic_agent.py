"""Synthetic agent — designs reaction pathways, retrosynthesis, and yields."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthesis import (RetrosynthesisEngine, ReactionPlanner, YieldPredictor,
                       ProtectingGroups, StereocontrolPlanner, PurificationPlanner,
                       ScaleupCalculator)
from src.gemini_25_flash_engine import reason as gemini25_reason


class SyntheticAgent:
    """Orchestrates synthesis capabilities."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.retro = RetrosynthesisEngine(api_key=api_key)
        self.planner = ReactionPlanner(api_key=api_key)
        self.yield_pred = YieldPredictor()
        self.protecting = ProtectingGroups()
        self.stereo = StereocontrolPlanner()
        self.purification = PurificationPlanner()
        self.scaleup = ScaleupCalculator()

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        text = task.lower()
        if "retro" in text:
            return {"agent": "SyntheticAgent", "capability": "retrosynthesis",
                    "result": self.retro.disconnect(params.get("smiles", task))}
        if "protect" in text:
            return {"agent": "SyntheticAgent", "capability": "protecting_groups",
                    "result": self.protecting.recommend(params.get("functional_group", "alcohol"),
                                                        params.get("conditions", []))}
        if "stereo" in text or "enantio" in text:
            return {"agent": "SyntheticAgent", "capability": "stereocontrol",
                    "result": self.stereo.recommend(params.get("transformation"))}
        if "purif" in text or "chromat" in text or "recrystall" in text:
            return {"agent": "SyntheticAgent", "capability": "purification",
                    "result": self.purification.column_chromatography(params.get("mass_g", 1.0))}
        if "scale" in text:
            return {"agent": "SyntheticAgent", "capability": "scaleup",
                    "result": self.scaleup.scale(params.get("lab_g", 1.0), params.get("target_g", 100.0))}
        if "yield" in text:
            return {"agent": "SyntheticAgent", "capability": "yield_prediction",
                    "result": self.yield_pred.predict(params.get("reaction", "Suzuki"),
                                                      params.get("T", 25), params.get("equiv", 1.0),
                                                      params.get("cat_loading", 0.05))}
        # Default: full reaction plan
        rt = params.get("reaction_type", "Suzuki")
        return {"agent": "SyntheticAgent", "capability": "reaction_planning",
                "result": self.planner.plan(rt)}

    def design_route(self, target_smiles, reaction_type="Suzuki"):
        """End-to-end route design."""
        return {
            "agent": "SyntheticAgent",
            "target": target_smiles,
            "retrosynthesis": self.retro.disconnect(target_smiles),
            "plan": self.planner.plan(reaction_type, target=target_smiles),
            "predicted_yield": self.yield_pred.predict(reaction_type),
            "purification": self.purification.column_chromatography(1.0),
        }
