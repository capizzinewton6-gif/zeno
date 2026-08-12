"""Improvement engine: improves existing inventions."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ImprovementEngine:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def improve(self, invention: str, goals: list[str] | None = None) -> str:
        g = ", ".join(goals) if goals else "efficiency, cost, reliability, sustainability"
        return self.engine.generate(
            f"Improve this invention targeting {g}. List concrete modifications "
            f"and expected benefits:\n{invention}",
            system="You are an invention improvement specialist.")

    def benchmark(self, invention: str) -> str:
        return self.engine.generate(
            f"Benchmark this invention against state of the art and identify gaps:\n{invention}",
            system="You are a competitive analyst.")

    def modernize(self, invention: str) -> str:
        return self.engine.generate(
            f"Modernize this invention with current technology (AI, IoT, new materials):\n{invention}",
            system="You are a technology modernization engineer.")
