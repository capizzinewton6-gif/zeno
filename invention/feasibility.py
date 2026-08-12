"""Feasibility analysis: technical, economic, manufacturing, and regulatory."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class FeasibilityAnalyzer:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def analyze(self, concept: str) -> str:
        return self.engine.generate(
            f"Analyze feasibility across scientific, technical, manufacturing, "
            f"economic, and regulatory dimensions. Give a verdict and risk rating "
            f"for: {concept}",
            system="You are a feasibility analyst.")

    def technical(self, concept: str) -> str:
        return self.engine.generate(
            f"Assess technical feasibility and identify showstoppers for: {concept}",
            system="You are a technical feasibility reviewer.")

    def economic(self, concept: str) -> str:
        return self.engine.generate(
            f"Assess economic feasibility (market, cost, ROI) for: {concept}",
            system="You are a techno-economic analyst.")

    def regulatory(self, concept: str) -> str:
        return self.engine.generate(
            f"Identify applicable regulations and certifications for: {concept}",
            system="You are a regulatory affairs specialist.")
