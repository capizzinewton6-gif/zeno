"""Civil engineering capability: structures, foundations, and infrastructure."""

from __future__ import annotations

from ai_core.knowledge_engine import KnowledgeEngine


class CivilEngineering:
    def __init__(self, knowledge: KnowledgeEngine | None = None):
        self.knowledge = knowledge or KnowledgeEngine()

    def structural_design(self, spec: str) -> str:
        return self.knowledge.engine.generate(
            f"Design a structure: {spec}. Include load paths, member sizing, codes.",
            system="You are a structural engineer.")

    def foundation_design(self, load: float, soil: str) -> str:
        return self.knowledge.engine.generate(
            f"Design a foundation for load {load} kN on {soil} soil.",
            system="You are a geotechnical engineer.")

    def concrete_mix(self, strength: float, application: str) -> str:
        return self.knowledge.engine.generate(
            f"Design a concrete mix for {strength} MPa for {application}.",
            system="You are a concrete technologist.")

    def site_plan(self, spec: str) -> str:
        return self.knowledge.engine.generate(
            f"Produce a site plan: {spec}.",
            system="You are a civil site engineer.")

    def load_calc(self, structure: str) -> str:
        return self.knowledge.engine.generate(
            f"Calculate dead, live, wind, and seismic loads for: {structure}.",
            system="You are a structural loading engineer.")
