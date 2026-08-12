"""Optimization agent: improves designs and efficiency."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from materials import MaterialSelector, MaterialDatabase


class OptimizationAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.material_selector = MaterialSelector(self.engine.primary)

    def optimize(self, design: str, objectives: str) -> str:
        return self.engine.reason(
            f"Optimize this design for: {objectives}. Provide trade-off "
            f"analysis (cost, weight, strength, efficiency, reliability):\n{design}",
            system="You are an engineering optimization specialist.")

    def multi_objective(self, design: str, weights: dict) -> str:
        w_str = ", ".join(f"{k}={v}" for k, v in weights.items())
        return self.engine.reason(
            f"Perform multi-objective optimization on:\n{design}\nWeights: {w_str}",
            system="You are a multi-objective optimization engineer.")

    def suggest_materials(self, design: str) -> str:
        return self.engine.reason(
            f"Recommend optimal materials for: {design}",
            system="You are a materials optimization engineer.")

    def lightweight(self, design: str) -> str:
        return self.engine.reason(
            f"Lightweight this design while preserving strength: {design}",
            system="You are a lightweighting engineer.")
