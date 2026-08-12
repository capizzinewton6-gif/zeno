"""Invention idea generator: produces original invention concepts."""

from __future__ import annotations

from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine


class IdeaGenerator:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def generate(self, problem: str, n: int = 5) -> List[str]:
        text = self.engine.generate(
            f"Generate {n} original, patentable invention ideas to solve: {problem}. "
            f"One per line, numbered.",
            system="You are a world-class inventor. Be novel and feasible.")
        return [l for l in text.splitlines() if l.strip()]

    def combine(self, ideas: List[str]) -> str:
        return self.engine.generate(
            f"Synthesize a single superior invention from these ideas:\n"
            + "\n".join(ideas),
            system="You are an invention synthesis engine.")

    def diverge(self, seed: str, n: int = 5) -> List[str]:
        return self.generate(seed, n)
