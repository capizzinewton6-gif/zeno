"""Circuit reader: analyzes circuits from image/description."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class CircuitReader:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def read(self, schematic_description: str) -> str:
        return self.engine.generate(
            f"Analyze this circuit schematic: topology, components, connections, "
            f"function:\n{schematic_description}",
            system="You are a circuit analyst.")

    def netlist(self, schematic_description: str) -> str:
        return self.engine.generate(
            f"Extract a netlist (component, node connections) from: {schematic_description}",
            system="You are a netlist extractor.")

    def function(self, schematic_description: str) -> str:
        return self.engine.generate(
            f"Identify the circuit function and operating principle from: "
            f"{schematic_description}",
            system="You are a circuit function analyst.")
