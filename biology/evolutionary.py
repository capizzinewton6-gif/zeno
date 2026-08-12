"""Phylogenetics, adaptation, and speciation."""
from __future__ import annotations

import math

from biology._shared import safe_ai_reason


class EvolutionaryModule:
    def handle(self, command: str, query: str, ctx) -> str:
        return safe_ai_reason(query, ctx)

    @staticmethod
    def jukes_cantor_distance(p: float) -> float:
        """JC69 nucleotide distance given proportion of differences p."""
        import math
        if p <= 0:
            return 0.0
        if p >= 0.75:
            return float("inf")
        return -0.75 * math.log(1 - (4 / 3) * p)

    @staticmethod
    def selection_coefficient(fitness_a: float, fitness_b: float) -> float:
        if fitness_b == 0:
            raise ValueError("Reference fitness must be > 0")
        return (fitness_a - fitness_b) / fitness_b

    @staticmethod
    def fixation_probability_beneficial(s: float, ne: int) -> float:
        if s <= 0:
            return 0.0
        return (1 - math.exp(-2 * s)) / (1 - math.exp(-2 * ne * s))
