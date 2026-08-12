"""Material strength analysis."""

from __future__ import annotations

import math

from .material_database import MaterialDatabase


class MaterialStrength:
    def __init__(self, db: MaterialDatabase | None = None):
        self.db = db or MaterialDatabase()

    def tensile_stress(self, force: float, area: float) -> float:
        return force / area

    def safety_factor(self, material: str, applied_stress: float) -> float | None:
        m = self.db.get(material)
        if not m:
            return None
        return m["yield_strength"] / applied_stress if applied_stress else float("inf")

    def critical_buckling(self, material: str, E: float, I: float, L: float,
                           k: float = 1.0) -> float:
        return math.pi ** 2 * E * I / (k * L) ** 2

    def fatigue_estimate(self, material: str, stress_amplitude: float,
                          ultimate_strength: float | None = None) -> float | None:
        m = self.db.get(material)
        if not m:
            return None
        u = ultimate_strength or m["ultimate_strength"]
        endurance = 0.5 * u  # rough S-N endurance limit for steels
        if stress_amplitude >= endurance:
            return 0.0
        return float("inf")

    def von_mises(self, sx: float, sy: float, txy: float) -> float:
        """Equivalent von Mises stress."""
        return math.sqrt(sx ** 2 - sx * sy + sy ** 2 + 3 * txy ** 2)
