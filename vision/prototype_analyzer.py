"""Prototype analyzer: analyzes prototype images/descriptions."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class PrototypeAnalyzer:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def analyze(self, prototype_description: str) -> str:
        return self.engine.generate(
            f"Analyze this prototype: build quality, assembly, wiring, "
            f"potential issues:\n{prototype_description}",
            system="You are a prototype QA engineer.")

    def fit_check(self, prototype_description: str, design: str) -> str:
        return self.engine.generate(
            f"Compare prototype:\n{prototype_description}\nto design:\n{design}\n"
            f"and report deviations.",
            system="You are a prototype verification engineer.")

    def improvements(self, prototype_description: str) -> str:
        return self.engine.generate(
            f"Recommend improvements for this prototype: {prototype_description}",
            system="You are a prototype improvement engineer.")
