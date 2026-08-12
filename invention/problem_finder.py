"""Problem finder: identifies problems worth solving."""

from __future__ import annotations

from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ProblemFinder:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def find(self, domain: str, n: int = 5) -> List[str]:
        text = self.engine.generate(
            f"Identify {n} important unsolved problems in {domain} worth inventing "
            f"for. One per line, numbered, with brief justification.",
            system="You are a research problem scout.")
        return [l for l in text.splitlines() if l.strip()]

    def pain_points(self, process: str) -> str:
        return self.engine.generate(
            f"Identify pain points and inefficiencies in: {process}.",
            system="You are a problem discovery analyst.")

    def trends(self, field: str) -> str:
        return self.engine.generate(
            f"Identify emerging trends creating invention opportunities in: {field}.",
            system="You are a technology trend analyst.")
