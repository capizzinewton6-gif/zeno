"""Simulation agent: runs engineering simulations."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from simulation import SimulationManager


class SimulationAgent:
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()
        self.manager = SimulationManager()

    def plan_simulations(self, design: str) -> str:
        return self.engine.reason(
            f"Identify which simulations (structural, thermal, fluid, circuit, "
            f"motion) are needed to validate: {design}",
            system="You are a CAE simulation planner.")

    def projectile(self, v0: float, angle: float):
        return self.manager.physics.projectile(v0, angle)

    def circuit_rc(self, v: float, r: float, c: float):
        return self.manager.circuit.rc_transient(v, r, c)

    def thermal(self, k: float, area: float, thickness: float, th: float, tc: float):
        return self.manager.thermal.steady_conduction_wall(k, area, thickness, th, tc)

    def interpret(self, results: str) -> str:
        return self.engine.reason(
            f"Interpret these simulation results and recommend design changes: {results}",
            system="You are a simulation analyst.")
