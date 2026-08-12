"""Thermal properties of materials."""

from __future__ import annotations

from .material_database import MaterialDatabase


class ThermalProperties:
    def __init__(self, db: MaterialDatabase | None = None):
        self.db = db or MaterialDatabase()

    def conductivity(self, material: str) -> float | None:
        m = self.db.get(material)
        return m["thermal_conductivity"] if m else None

    def heat_capacity(self, material: str) -> float | None:
        m = self.db.get(material)
        return m["specific_heat"] if m else None

    def thermal_diffusivity(self, material: str) -> float | None:
        m = self.db.get(material)
        if not m:
            return None
        return m["thermal_conductivity"] / (m["density"] * m["specific_heat"])

    def thermal_resistance(self, material: str, thickness: float, area: float) -> float | None:
        m = self.db.get(material)
        if not m:
            return None
        return thickness / (m["thermal_conductivity"] * area)

    def expansion_fit(self, material_a: str, material_b: str) -> str:
        a = self.db.get(material_a)
        b = self.db.get(material_b)
        if not a or not b:
            return "Material not found"
        if abs(a["thermal_conductivity"] - b["thermal_conductivity"]) < 20:
            return "Thermally compatible"
        return "Thermal mismatch - design compensation needed"
