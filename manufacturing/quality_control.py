"""Quality control planning."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class QualityControl:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def plan(self, product: str) -> str:
        return self.engine.generate(
            f"Design a quality control plan (inspections, sampling, AQL, "
            f"instruments) for: {product}.",
            system="You are a QC engineer.")

    def cpk(self, usl: float, lsl: float, mean: float, std: float) -> float:
        if std == 0:
            return float("inf")
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        return min(cpu, cpl)

    def sample_size(self, lot: int, aql: float = 1.0) -> int:
        """Simplified single sampling plan size."""
        if lot <= 8:
            return min(lot, 5)
        if lot <= 150:
            return 20
        if lot <= 500:
            return 50
        return 80

    def defects_ppm(self, defects: int, sample: int) -> float:
        return (defects / sample) * 1e6 if sample else 0

    def six_sigma_shift(self, mean: float, target: float, std: float) -> float:
        """Sigma shift from target."""
        return abs(mean - target) / std if std else 0
