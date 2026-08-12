"""Component identifier: identifies electronic/mechanical components."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class ComponentIdentifier:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def identify(self, description: str) -> str:
        return self.engine.generate(
            f"Identify the component(s) from this description/marking: {description}. "
            f"Give part number, type, and key specs.",
            system="You are a component identification engineer.")

    def from_marking(self, marking: str) -> str:
        return self.engine.generate(
            f"Decode this component marking/code: {marking}",
            system="You are a component marking decoder.")

    def from_footprint(self, footprint: str) -> str:
        return self.engine.generate(
            f"Identify the package/footprint: {footprint}",
            system="You are a packaging specialist.")
