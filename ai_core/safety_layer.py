"""Engineering safety layer: validates designs against safety principles,
applies safety factors, and flags hazards."""

from __future__ import annotations

from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine

# Conservative default safety factors (dimensionless).
DEFAULT_SAFETY_FACTORS = {
    "yield_strength": 2.0,
    "ultimate_strength": 3.0,
    "fatigue": 4.0,
    "buckling": 2.5,
    "thermal": 1.5,
    "electrical_insulation": 2.0,
}


class SafetyLayer:
    def __init__(self, engine: Gemini25FlashEngine | None = None,
                 safety_factors: dict | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.safety_factors = safety_factors or DEFAULT_SAFETY_FACTORS

    def apply_factor(self, value: float, category: str) -> float:
        factor = self.safety_factors.get(category, 2.0)
        return value / factor

    def analyze(self, design_description: str) -> str:
        return self.engine.generate(
            f"Perform a safety analysis (hazard identification, risk rating, "
            f"mitigations, regulatory notes) for: {design_description}",
            system="You are a safety engineer. Be conservative and thorough.")

    def check_calculations(self, calc_summary: str) -> str:
        return self.engine.generate(
            f"Review these engineering calculations for safety and correctness. "
            f"Verify safety factors are applied: {calc_summary}",
            system="You are a calculation safety reviewer.")

    def hazard_checklist(self, system: str) -> List[str]:
        text = self.engine.generate(
            f"Produce a hazard checklist (one item per line) for: {system}",
            system="You are a safety engineer.")
        return [l for l in text.splitlines() if l.strip()]
