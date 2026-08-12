"""Cost estimator: manufacturing and product cost estimation."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class CostEstimator:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def estimate(self, design: str, volume: int = 1) -> str:
        return self.engine.generate(
            f"Estimate manufacturing cost (materials, labor, tooling, overhead) "
            f"for {volume} units of: {design}.",
            system="You are a cost estimation engineer.")

    def unit_cost(self, materials: float, labor: float, overhead: float,
                  tooling: float, volume: int) -> float:
        return (materials + labor + overhead) + (tooling / volume if volume else float("inf"))

    def breakdown(self, materials: float, labor: float, overhead: float,
                  tooling: float, volume: int) -> dict:
        total = materials + labor + overhead + tooling / max(volume, 1)
        return {
            "materials": materials, "labor": labor, "overhead": overhead,
            "tooling_per_unit": tooling / max(volume, 1),
            "unit_cost": round(total, 2),
        }

    def roi(self, unit_cost: float, sale_price: float, volume: int,
            fixed_costs: float) -> dict:
        profit_per = sale_price - unit_cost
        break_even = fixed_costs / profit_per if profit_per > 0 else float("inf")
        return {"profit_per_unit": round(profit_per, 2),
                "break_even_units": round(break_even),
                "annual_profit": round(profit_per * volume - fixed_costs, 2)}
