"""Material selector: Ashby-style selection."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine
from .material_database import MaterialDatabase


class MaterialSelector:
    def __init__(self, engine: Gemini25FlashEngine | None = None,
                 db: MaterialDatabase | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.db = db or MaterialDatabase()

    def select(self, application: str, constraints: str = "") -> str:
        return self.engine.generate(
            f"Select materials for: {application}. Constraints: {constraints}. "
            f"Justify with property data and Ashby charts.",
            system="You are a materials selection engineer.")

    def by_strength_to_weight(self, top: int = 3) -> list[dict]:
        ranked = sorted(self.db.materials,
                        key=lambda m: m["yield_strength"] / m["density"], reverse=True)
        return [{"name": m["name"],
                 "specific_strength": m["yield_strength"] / m["density"]}
                for m in ranked[:top]]

    def by_stiffness_to_weight(self, top: int = 3) -> list[dict]:
        ranked = sorted(self.db.materials,
                        key=lambda m: m["youngs_modulus"] / m["density"], reverse=True)
        return [{"name": m["name"],
                 "specific_modulus": m["youngs_modulus"] / m["density"]}
                for m in ranked[:top]]

    def cheapest(self, top: int = 3) -> list[dict]:
        ranked = sorted(self.db.materials, key=lambda m: m["cost_per_kg"])
        return [{"name": m["name"], "cost_per_kg": m["cost_per_kg"]}
                for m in ranked[:top]]

    def best_thermal_conductor(self, top: int = 3) -> list[dict]:
        ranked = sorted(self.db.materials,
                        key=lambda m: m["thermal_conductivity"], reverse=True)
        return [{"name": m["name"],
                 "thermal_conductivity": m["thermal_conductivity"]}
                for m in ranked[:top]]
