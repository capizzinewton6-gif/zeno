"""Technology search and benchmarking."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class TechnologySearch:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def search(self, need: str) -> str:
        return self.engine.generate(
            f"Identify candidate technologies that solve: {need}. Include TRL, "
            f"vendors, specs.",
            system="You are a technology scout.")

    def benchmark(self, technologies: list[str]) -> str:
        return self.engine.generate(
            f"Benchmark these technologies across performance, cost, maturity: "
            f"{', '.join(technologies)}.",
            system="You are a technology benchmarking engineer.")

    def roadmap(self, technology: str) -> str:
        return self.engine.generate(
            f"Produce a technology roadmap for: {technology}.",
            system="You are a technology strategist.")
