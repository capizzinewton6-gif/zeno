"""Manufacturing planner: end-to-end production planning."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ManufacturingPlanner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def plan(self, design: str, volume: int = 1) -> str:
        return self.engine.generate(
            f"Create a manufacturing plan for: {design} at volume {volume} units. "
            f"Cover process, sequence, tooling, quality, lead time.",
            system="You are a manufacturing engineer.")

    def production_line(self, product: str, volume: int) -> str:
        return self.engine.generate(
            f"Design a production line for {volume} units/yr of: {product}.",
            system="You are a production engineer.")

    def lead_time(self, plan: str) -> str:
        return self.engine.generate(
            f"Estimate lead times and bottlenecks for this plan:\n{plan}",
            system="You are a production scheduler.")
