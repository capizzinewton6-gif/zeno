"""Electronics prototype: breadboard/perfboard planning."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ElectronicsPrototype:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def breadboard_plan(self, circuit: str) -> str:
        return self.engine.generate(
            f"Produce a breadboard layout plan for: {circuit}.",
            system="You are an electronics prototyping engineer.")

    def wiring_plan(self, circuit: str) -> str:
        return self.engine.generate(
            f"Produce a wiring/connection plan for: {circuit}.",
            system="You are an electronics technician.")

    def test_points(self, circuit: str) -> str:
        return self.engine.generate(
            f"Identify test points and expected signals for: {circuit}.",
            system="You are a test engineer.")

    def power_distribution(self, circuit: str) -> str:
        return self.engine.generate(
            f"Design power distribution and decoupling for: {circuit}.",
            system="You are a power distribution engineer.")
