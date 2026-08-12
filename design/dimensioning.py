"""Engineering dimensioning: assigns and annotates dimensions."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine

# Default ISO 2768 general tolerances (medium).
DEFAULT_TOLERANCES = {
    "linear_0_6": 0.1,
    "linear_6_30": 0.2,
    "linear_30_120": 0.3,
    "linear_120_400": 0.5,
    "angular": 1.0,
}


class Dimensioning:
    def __init__(self, engine: Gemini25FlashEngine | None = None,
                 tolerances: dict | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.tolerances = tolerances or DEFAULT_TOLERANCES

    def recommend(self, concept: str) -> str:
        return self.engine.generate(
            f"Recommend key dimensions, datums, and tolerances for: {concept}",
            system="You are a GD&T engineer following ISO 2768 / ASME Y14.5.")

    def fit(self, hole: float, shaft: float) -> dict:
        """Return basic fit classification for hole/shaft nominal pair."""
        diff = hole - shaft
        if diff > 0:
            return {"type": "clearance", "clearance_mm": round(diff, 4)}
        if diff < 0:
            return {"type": "interference", "interference_mm": round(-diff, 4)}
        return {"type": "transition", "difference_mm": 0.0}

    def tolerance_for(self, dimension: float) -> float:
        if dimension <= 6:
            return self.tolerances["linear_0_6"]
        if dimension <= 30:
            return self.tolerances["linear_6_30"]
        if dimension <= 120:
            return self.tolerances["linear_30_120"]
        return self.tolerances["linear_120_400"]
