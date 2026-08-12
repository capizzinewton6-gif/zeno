"""Engineering reasoning engine: applies first-principles, multi-disciplinary
reasoning to engineering problems via the primary Gemini engine."""

from __future__ import annotations

from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ReasoningEngine:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def reason(self, problem: str, discipline: str = "general") -> str:
        return self.engine.generate(
            f"[{discipline}] Reason through this engineering problem step by step, "
            f"stating assumptions and governing equations: {problem}",
            system="You are an expert engineering reasoning engine.")

    def first_principles(self, problem: str) -> str:
        return self.engine.generate(
            f"Derive a solution from first principles for: {problem}",
            system="Use physics and chemistry fundamentals.")

    def multi_disciplinary(self, problem: str, disciplines: List[str]) -> str:
        d = ", ".join(disciplines)
        return self.engine.generate(
            f"Analyse this problem across [{d}] and propose an integrated solution: {problem}",
            system="You are a multi-disciplinary engineering team.")

    def trade_off_analysis(self, options: List[str], criteria: List[str]) -> str:
        return self.engine.generate(
            f"Compare options {options} against criteria {criteria} in a decision matrix.",
            system="You are a trade-off analysis expert.")
