"""Main engineering agent: orchestrates engineering intelligence."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from ai_core.knowledge_engine import KnowledgeEngine
from engineering import MechanicalEngineering, ElectricalEngineering, ElectronicsEngineering
from calculations import Mechanics, Electricity, Circuits


class EngineeringAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.knowledge = KnowledgeEngine(self.engine.primary)
        self.mechanical = MechanicalEngineering(self.knowledge)
        self.electrical = ElectricalEngineering(self.knowledge)
        self.electronics = ElectronicsEngineering(self.knowledge)
        self.mechanics_calc = Mechanics()
        self.electricity_calc = Electricity()
        self.circuits_calc = Circuits()

    def solve(self, problem: str) -> str:
        return self.engine.reason(
            f"Decompose and solve this engineering problem, applying mechanical, "
            f"electrical, and electronic analysis: {problem}",
            system="You are a principal engineering agent.")

    def analyze(self, system: str) -> str:
        return self.engine.reason(
            f"Analyze this engineering system across disciplines: {system}",
            system="You are a multidisciplinary engineering analyst.")

    def design_review(self, design: str) -> str:
        return self.engine.reason(
            f"Review this engineering design for correctness, safety, and "
            f"optimization: {design}",
            system="You are a senior design reviewer.")
