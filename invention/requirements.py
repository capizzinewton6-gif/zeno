"""Requirements definition: derives structured engineering requirements."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class RequirementsDefiner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def define(self, concept: str) -> str:
        return self.engine.generate(
            f"Define functional, performance, interface, environmental, safety, "
            f"and regulatory requirements for: {concept}",
            system="You are a requirements engineer. Be specific and measurable.")

    def constraints(self, concept: str) -> str:
        return self.engine.generate(
            f"List design constraints (cost, size, mass, power, manufacturing) for: {concept}",
            system="You are a constraints analyst.")

    def acceptance(self, requirements: str) -> str:
        return self.engine.generate(
            f"Define acceptance criteria for these requirements:\n{requirements}",
            system="You are a verification engineer.")
