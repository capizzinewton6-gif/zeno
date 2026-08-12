"""Circuit designer: designs electronic circuits via the primary engine."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class CircuitDesigner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def design(self, spec: str) -> str:
        return self.engine.generate(
            f"Design an electronic circuit for: {spec}. Provide schematic "
            f"description, BOM, and analysis.",
            system="You are a senior circuit designer.")

    def simulate_spec(self, spec: str) -> str:
        return self.engine.generate(
            f"Specify simulation parameters (sources, probes, analysis type) for: {spec}",
            system="You are an EDA engineer.")

    def layout_guidance(self, circuit: str) -> str:
        return self.engine.generate(
            f"Provide PCB layout guidance for: {circuit}",
            system="You are a PCB layout engineer.")
