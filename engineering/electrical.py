"""Electrical engineering capability: power systems, motors, generators,
and electrical machine design."""

from __future__ import annotations

from ai_core.knowledge_engine import KnowledgeEngine


class ElectricalEngineering:
    def __init__(self, knowledge: KnowledgeEngine | None = None):
        self.knowledge = knowledge or KnowledgeEngine()

    def power_system(self, spec: str) -> str:
        return self.knowledge.engine.generate(
            f"Design an electrical power system: {spec}. Include generation, "
            f"distribution, protection.",
            system="You are a power systems engineer.")

    def motor_selection(self, load: str, speed: float) -> str:
        return self.knowledge.engine.generate(
            f"Select a motor for load '{load}' at {speed} rpm. Specify type, "
            f"power, torque, control.",
            system="You are an electrical machines engineer.")

    def transformer_design(self, power: float, v1: float, v2: float) -> str:
        return self.knowledge.engine.generate(
            f"Design a transformer: {power} VA, primary {v1}V, secondary {v2}V.",
            system="You are a transformer design engineer.")

    def power_factor_correction(self, load_kw: float, pf: float, target_pf: float) -> str:
        import math
        needed = load_kw * (math.tan(math.acos(pf)) - math.tan(math.acos(target_pf)))
        return (f"Capacitive reactive power required: {needed:.2f} kVAR to raise "
                f"power factor from {pf} to {target_pf}.")

    def protection_coordination(self, system: str) -> str:
        return self.knowledge.engine.generate(
            f"Design protection and coordination for: {system}.",
            system="You are a protection engineer.")
