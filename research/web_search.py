"""Engineering web research via the primary engine."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class WebSearch:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def research(self, query: str) -> str:
        return self.engine.generate(
            f"Research the engineering topic: {query}. Summarize state of the art, "
            f"key technologies, and references.",
            system="You are an engineering researcher.")

    def compare(self, options: list[str]) -> str:
        joined = ", ".join(options)
        return self.engine.generate(
            f"Compare these engineering options in a table: {joined}. "
            f"Cover performance, cost, maturity, trade-offs.",
            system="You are a technology analyst.")

    def state_of_art(self, field: str) -> str:
        return self.engine.generate(
            f"Summarize the state of the art in: {field}.",
            system="You are a research analyst.")
