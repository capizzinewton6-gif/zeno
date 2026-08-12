"""Chemical engineering capability: reactors, separations, and process design."""

from __future__ import annotations

from ai_core.knowledge_engine import KnowledgeEngine


class ChemicalEngineering:
    def __init__(self, knowledge: KnowledgeEngine | None = None):
        self.knowledge = knowledge or KnowledgeEngine()

    def reactor_design(self, reaction: str, throughput: float) -> str:
        return self.knowledge.engine.generate(
            f"Design a reactor for reaction '{reaction}' at throughput {throughput}. "
            f"Specify type, kinetics, heat removal.",
            system="You are a chemical reactor engineer.")

    def separation_process(self, mixture: str, target: str) -> str:
        return self.knowledge.engine.generate(
            f"Design a separation to recover {target} from {mixture}.",
            system="You are a separation process engineer.")

    def mass_balance(self, process: str) -> str:
        return self.knowledge.engine.generate(
            f"Perform a mass and energy balance for: {process}.",
            system="You are a process engineer.")

    def process_flow_diagram(self, process: str) -> str:
        return self.knowledge.engine.generate(
            f"Describe a process flow diagram (streams, units) for: {process}.",
            system="You are a process design engineer.")

    def corrosion_control(self, environment: str, material: str) -> str:
        return self.knowledge.engine.generate(
            f"Recommend corrosion control for {material} in {environment}.",
            system="You are a corrosion engineer.")
