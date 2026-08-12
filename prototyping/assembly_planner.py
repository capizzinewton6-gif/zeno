"""Assembly planner: assembly sequence and instructions."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class AssemblyPlanner:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def sequence(self, parts: list[str]) -> str:
        joined = "\n".join(parts)
        return self.engine.generate(
            f"Determine an assembly sequence (DFA) for these parts:\n{joined}",
            system="You are a DFA engineer.")

    def instructions(self, design: str) -> str:
        return self.engine.generate(
            f"Write step-by-step assembly instructions for: {design}.",
            system="You are a technical writer for assembly.")

    def tools_fixtures(self, design: str) -> str:
        return self.engine.generate(
            f"List required tools and fixtures for assembling: {design}.",
            system="You are a manufacturing engineer.")

    def time_estimate(self, design: str) -> str:
        return self.engine.generate(
            f"Estimate assembly time per unit for: {design}.",
            system="You are an industrial engineer.")
