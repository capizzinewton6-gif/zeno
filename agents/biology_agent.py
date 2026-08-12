"""Main biological intelligence agent that routes requests to domain modules."""
from __future__ import annotations

import re

from ai_core.ai_engine import AIEngine
from ai_core.context_manager import ContextManager
from ai_core.safety_layer import SafetyLayer


class BiologyAgent:
    """Top-level agent selecting required capability modules and routing tasks."""

    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()
        self.ctx = ContextManager()
        self.safety = SafetyLayer()
        self.modules = self._wire_modules()

    def _wire_modules(self) -> dict:
        from biology.molecular import MolecularModule
        from biology.genetics import GeneticsModule
        from biology.cell_biology import CellBiologyModule
        from biology.biochemistry import BiochemistryModule
        from biology.ecology import EcologyModule
        from biology.evolutionary import EvolutionaryModule
        from biology.microbiology import MicrobiologyModule
        from biology.immunology import ImmunologyModule
        from biology.bioinformatics import BioinformaticsModule
        return {
            "molecular": MolecularModule(),
            "genetics": GeneticsModule(),
            "cell_biology": CellBiologyModule(),
            "biochemistry": BiochemistryModule(),
            "ecology": EcologyModule(),
            "evolutionary": EvolutionaryModule(),
            "microbiology": MicrobiologyModule(),
            "immunology": ImmunologyModule(),
            "bioinformatics": BioinformaticsModule(),
        }

    def route(self, query: str) -> str:
        verdict = self.safety.screen_text(query)
        if not verdict:
            return f"[SAFETY BLOCK] {verdict.reason}"
        module_key, command = self._classify(query)
        module = self.modules.get(module_key)
        if module is None:
            return self.ai.reason(query, system=self.ctx.context_string())
        try:
            return module.handle(command, query, self.ctx)
        except AttributeError:
            return self.ai.reason(query, system=self.ctx.context_string())

    def _classify(self, query: str) -> tuple[str, str]:
        q = query.lower()
        rules = [
            ("molecular", ["dna", "rna", "transcri", "translat", "pcr", "primer", "restriction", "plasmid"]),
            ("genetics", ["mendel", "allele", "genotype", "hardy", "weinberg", "heritab", "punnett"]),
            ("cell_biology", ["cell cycle", "mitosis", "meiosis", "organelle", "signal", "apoptosis", "membrane"]),
            ("biochemistry", ["enzyme", "kinetic", "michaelis", "km", "vmax", "metabol", "atp", "glycolysis"]),
            ("ecology", ["ecosystem", "population", "biodivers", "trophic", "predator", "niche", "conservation"]),
            ("evolutionary", ["evolution", "phylogen", "speciation", "adaptation", "selection", "drift", "fitness"]),
            ("microbiology", ["bacteri", "virus", "fungi", "culture", "gram", "colony", "biofilm"]),
            ("immunology", ["immune", "antibody", "antigen", "t cell", "cytokine", "vaccine", "innate"]),
            ("bioinformatics", ["align", "blast", "fasta", "genbank", "motif", "sequence analysis", "ortholog"]),
        ]
        for key, keywords in rules:
            if any(kw in q for kw in keywords):
                return key, query
        return "molecular", query

    def status(self) -> dict:
        return {"modules": list(self.modules), "context": self.ctx.context_string(),
                "ai": self.ai.status()}
