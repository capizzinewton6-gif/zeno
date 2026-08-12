"""CNC manufacturing: toolpath and machining planning."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class CNC:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def plan(self, part: str, material: str) -> str:
        return self.engine.generate(
            f"Create a CNC machining plan (operations, tools, feeds/speeds, fixtures) "
            f"for {part} in {material}.",
            system="You are a CNC manufacturing engineer.")

    def feeds_speeds(self, material: str, tool_diameter: float,
                     flutes: int = 2) -> dict:
        # Very rough heuristic cutting parameters by material.
        base = {"aluminum": {"speed": 300, "feed": 0.05},
                "steel": {"speed": 100, "feed": 0.03},
                "plastic": {"speed": 500, "feed": 0.08}}.get(material.lower(),
                                                              {"speed": 200, "feed": 0.04})
        rpm = base["speed"] * 1000 / (math.pi * tool_diameter) if tool_diameter else 0
        feed_rate = rpm * flutes * base["feed"]
        return {"rpm": rpm, "feed_mm_per_min": feed_rate,
                "chipload_mm": base["feed"], "material": material}

    def toolpath_strategy(self, feature: str) -> str:
        return self.engine.generate(
            f"Recommend CNC toolpath strategy for feature: {feature}.",
            system="You are a CAM engineer.")
