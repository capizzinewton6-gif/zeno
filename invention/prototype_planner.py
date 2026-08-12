"""Prototype planner: plans physical and virtual prototypes."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class PrototypePlanner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def plan(self, concept: str) -> str:
        return self.engine.generate(
            f"Plan a staged prototype program (alpha, beta, validation) for: {concept}. "
            f"Include goals, methods, and success criteria per stage.",
            system="You are a prototype planning engineer.")

    def mvp(self, concept: str) -> str:
        return self.engine.generate(
            f"Define the minimum viable prototype to de-risk the core function of: {concept}",
            system="You are an MVP engineer.")

    def test_plan(self, concept: str) -> str:
        return self.engine.generate(
            f"Create a test plan (functional, performance, reliability, safety) for: {concept}",
            system="You are a test engineer.")
