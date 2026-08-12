"""Electrical properties of materials."""

from __future__ import annotations

from .material_database import MaterialDatabase

# Conductivity (S/m) and resistivity (ohm.m) for common conductors/insulators.
ELECTRICAL_DATA = {
    "Copper": {"conductivity": 5.96e7, "resistivity": 1.68e-8},
    "Aluminum 6061-T6": {"conductivity": 3.5e7, "resistivity": 2.86e-8},
    "Stainless 304": {"conductivity": 1.37e6, "resistivity": 7.3e-7},
    "Steel AISI 1045": {"conductivity": 7.7e6, "resistivity": 1.3e-7},
    "ABS Plastic": {"conductivity": 1e-14, "resistivity": 1e14},
    "PLA": {"conductivity": 1e-15, "resistivity": 1e15},
    "Carbon Fiber Composite": {"conductivity": 1e4, "resistivity": 1e-4},
    "Titanium Grade 5": {"conductivity": 5.6e5, "resistivity": 1.78e-6},
}


class ElectricalProperties:
    def __init__(self, db: MaterialDatabase | None = None):
        self.db = db or MaterialDatabase()

    def conductivity(self, material: str) -> float | None:
        data = ELECTRICAL_DATA.get(material)
        return data["conductivity"] if data else None

    def resistivity(self, material: str) -> float | None:
        data = ELECTRICAL_DATA.get(material)
        return data["resistivity"] if data else None

    def wire_resistance(self, material: str, length: float, area: float) -> float | None:
        rho = self.resistivity(material)
        if rho is None:
            return None
        return rho * length / area

    def is_conductor(self, material: str, threshold: float = 1e5) -> bool | None:
        cond = self.conductivity(material)
        return cond is not None and cond > threshold

    def is_insulator(self, material: str, threshold: float = 1e-10) -> bool | None:
        cond = self.conductivity(material)
        return cond is not None and cond < threshold
