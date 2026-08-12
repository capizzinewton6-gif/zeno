"""Materials selection for design."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class DesignMaterials:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def select(self, application: str, constraints: str = "") -> str:
        return self.engine.generate(
            f"Select suitable materials for: {application}. Constraints: {constraints}. "
            f"Justify with properties (strength, density, thermal, cost).",
            system="You are a materials selection engineer using Ashby methods.")

    def compare(self, materials: list[str], criteria: list[str]) -> str:
        return self.engine.generate(
            f"Compare materials {materials} on {criteria} in a table.",
            system="You are a materials comparison engineer.")

    def ashby_chart_data(self, materials: list[dict]) -> list[dict]:
        """Return density vs strength points for an Ashby-style chart."""
        return [{"name": m["name"], "density": m.get("density", 0),
                 "strength": m.get("strength", 0)} for m in materials]
