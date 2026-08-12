"""Geneticist agent: designs gene edits, primers, and constructs."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine
from ai_core.context_manager import ContextManager
from ai_core.safety_layer import SafetyLayer


class GeneticistAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()
        self.ctx = ContextManager()
        self.safety = SafetyLayer()

    def design_crispr(self, target_sequence: str, pam: str = "NGG") -> dict:
        from genetic_engineering.crispr_designer import CRISPRDesigner
        verdict = self.safety.screen_sequence(target_sequence)
        if not verdict:
            return {"error": verdict.reason}
        return CRISPRDesigner().design_grna(target_sequence, pam)

    def design_primers(self, template: str, product_size: int = 500) -> dict:
        from genetic_engineering.primer_designer import PrimerDesigner
        return PrimerDesigner().design_primers(template, product_size)

    def build_plasmid(self, insert: str, vector: str = "pUC19") -> dict:
        from genetic_engineering.plasmid_builder import PlasmidBuilder
        return PlasmidBuilder().build(insert, vector)

    def optimize_codons(self, protein_seq: str, host: str = "escherichia coli") -> dict:
        from genetic_engineering.codon_optimizer import CodonOptimizer
        return CodonOptimizer().optimize(protein_seq, host)

    def plan_cloning(self, goal: str) -> list[dict]:
        from ai_core.planning_engine import PlanningEngine
        return PlanningEngine(self.ai).plan_cloning(goal)

    def explain_design(self, design: dict) -> str:
        return self.ai.reason(
            "Explain this genetic construct design to a researcher, noting the "
            "key design choices, expected function, and any risks:\n\n"
            + str(design)
        )
