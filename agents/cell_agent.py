"""Cell agent: analyzes cellular pathways and phenotypes."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine
from ai_core.context_manager import ContextManager


class CellAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()
        self.ctx = ContextManager()

    def analyze_pathway(self, pathway: str) -> dict:
        from biology.cell_biology import CellBiologyModule
        return CellBiologyModule().analyze_pathway(pathway)

    def predict_phenotype(self, genotype_change: str) -> str:
        return self.ai.reason(
            "Predict the most likely cellular phenotype resulting from this "
            "genotype change, reasoning through the affected pathway:\n\n"
            + genotype_change
        )

    def cell_cycle_phase(self, marker_profile: dict) -> str:
        from biology.cell_biology import CellBiologyModule
        return CellBiologyModule().cell_cycle_phase(marker_profile)
