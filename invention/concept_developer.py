"""Concept developer: expands raw ideas into detailed invention concepts."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ConceptDeveloper:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def develop(self, idea: str) -> str:
        return self.engine.generate(
            f"Develop this invention idea into a detailed concept: principle of "
            f"operation, key components, novelty, advantages.\n{idea}",
            system="You are an invention concept developer.")

    def differentiate(self, concept: str, prior_art: str) -> str:
        return self.engine.generate(
            f"Given this concept:\n{concept}\nand prior art:\n{prior_art}\n"
            f"Sharpen the novelty and differentiation.",
            system="You are a patent-minded concept developer.")

    def narrative(self, concept: str) -> str:
        return self.engine.generate(
            f"Write a concise invention disclosure narrative for: {concept}",
            system="You are a technical writer for inventions.")
