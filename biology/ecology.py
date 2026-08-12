"""Ecosystems, biodiversity, and conservation."""
from __future__ import annotations

import math
from collections import Counter

from biology._shared import safe_ai_reason


class EcologyModule:
    def handle(self, command: str, query: str, ctx) -> str:
        return safe_ai_reason(query, ctx)

    @staticmethod
    def shannon_index(counts: list[int]) -> float:
        total = sum(counts)
        if total == 0:
            return 0.0
        h = 0.0
        for c in counts:
            if c > 0:
                p = c / total
                h -= p * math.log(p)
        return h

    @staticmethod
    def simpson_index(counts: list[int]) -> float:
        total = sum(counts)
        if total <= 1:
            return 0.0
        return 1.0 - sum((c / total) ** 2 for c in counts if c > 0)

    @staticmethod
    def species_richness(counts: list[int]) -> int:
        return sum(1 for c in counts if c > 0)

    @staticmethod
    def evenness(shannon_h: float, richness: int) -> float:
        if richness <= 1:
            return 0.0
        return shannon_h / math.log(richness)

    @staticmethod
    def lotka_volterra_step(prey, predator, alpha, beta, delta, gamma):
        d_prey = prey * (alpha - beta * predator)
        d_pred = predator * (-gamma + delta * prey)
        return prey + d_prey, predator + d_pred
