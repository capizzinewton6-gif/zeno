"""Diagram reader: understands technical diagrams."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class DiagramReader:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def read(self, diagram_description: str) -> str:
        return self.engine.generate(
            f"Interpret this technical diagram: type, elements, flows, "
            f"relationships:\n{diagram_description}",
            system="You are a technical diagram analyst.")

    def block_diagram(self, description: str) -> str:
        return self.engine.generate(
            f"Extract blocks and interconnections from: {description}",
            system="You are a system block analyst.")

    def flow(self, description: str) -> str:
        return self.engine.generate(
            f"Extract process/signal flow from: {description}",
            system="You are a flow analyst.")
