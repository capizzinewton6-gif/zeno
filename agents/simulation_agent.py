"""Simulation agent: runs population and molecular dynamics simulations."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine
from ai_core.context_manager import ContextManager


class SimulationAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()
        self.ctx = ContextManager()

    def run_lotka_volterra(self, prey0=40, predator0=9, alpha=0.1, beta=0.02,
                           delta=0.01, gamma=0.1, days=200):
        from simulation.population_simulator import LotkaVolterraSimulator
        return LotkaVolterraSimulator().run(
            prey0, predator0, alpha, beta, delta, gamma, days
        )

    def run_sir(self, population=10000, i0=1, beta=0.3, gamma=0.1, days=160):
        from simulation.viral_transmission import SIRModel
        return SIRModel().run(population, i0, beta, gamma, days)

    def run_metabolic_flux(self, reactions: list[dict], objective: str, maximize=True):
        from simulation.metabolic_flux_sim import FBASimulator
        return FBASimulator().run(reactions, objective, maximize)

    def run_evolution(self, population=1000, generations=100, fitness_advantage=0.05):
        from simulation.evolution_simulator import EvolutionSimulator
        return EvolutionSimulator().run(population, generations, fitness_advantage)

    def run_protein_dynamics(self, n_steps=1000, temperature=300):
        from simulation.protein_dynamics import ProteinDynamics
        return ProteinDynamics().run(n_steps, temperature)

    def run_cell_cycle(self, n_cells=100, cycles=5):
        from simulation.cell_cycle_simulator import CellCycleSimulator
        return CellCycleSimulator().run(n_cells, cycles)

    def explain(self, result: dict) -> str:
        return self.ai.reason(
            "Interpret these simulation results biologically and explain the key "
            "dynamics and any biological conclusions:\n\n" + str(result)[:3000]
        )
