"""Optimization agent: optimizes codon usage, growth, and yields."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine


class OptimizationAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()

    def optimize_codons(self, protein_seq: str, host: str = "escherichia coli") -> dict:
        from genetic_engineering.codon_optimizer import CodonOptimizer
        return CodonOptimizer().optimize(protein_seq, host)

    def optimize_growth_media(self, organism: str, target: str = "biomass") -> dict:
        from simulation.metabolic_flux_sim import FBASimulator
        return FBASimulator().optimize_media(organism, target)

    def optimize_yield(self, parameters: dict, response: list[float]) -> dict:
        from calculations.enzyme_kinetics import optimize_yield
        return optimize_yield(parameters, response)

    def recommend(self, analysis: dict) -> str:
        return self.ai.reason(
            "Given these optimization results, recommend concrete experimental "
            "changes to improve yield and explain the trade-offs:\n\n"
            + str(analysis)[:3000]
        )
