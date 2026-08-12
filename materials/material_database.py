"""Material database with common engineering materials."""

from __future__ import annotations

from typing import Any, Dict, List

# Built-in material properties (SI units).
MATERIALS: List[Dict[str, Any]] = [
    {"name": "Aluminum 6061-T6", "density": 2700, "yield_strength": 276e6,
     "ultimate_strength": 310e6, "youngs_modulus": 69e9, "poisson": 0.33,
     "thermal_conductivity": 167, "specific_heat": 896, "cost_per_kg": 3.0},
    {"name": "Steel AISI 1045", "density": 7850, "yield_strength": 530e6,
     "ultimate_strength": 625e6, "youngs_modulus": 200e9, "poisson": 0.29,
     "thermal_conductivity": 51.9, "specific_heat": 486, "cost_per_kg": 1.2},
    {"name": "Stainless 304", "density": 8000, "yield_strength": 215e6,
     "ultimate_strength": 505e6, "youngs_modulus": 193e9, "poisson": 0.29,
     "thermal_conductivity": 16.2, "specific_heat": 500, "cost_per_kg": 4.5},
    {"name": "Titanium Grade 5", "density": 4430, "yield_strength": 880e6,
     "ultimate_strength": 950e6, "youngs_modulus": 114e9, "poisson": 0.34,
     "thermal_conductivity": 6.7, "specific_heat": 526, "cost_per_kg": 25.0},
    {"name": "ABS Plastic", "density": 1050, "yield_strength": 40e6,
     "ultimate_strength": 45e6, "youngs_modulus": 2.0e9, "poisson": 0.35,
     "thermal_conductivity": 0.18, "specific_heat": 1900, "cost_per_kg": 2.0},
    {"name": "PLA", "density": 1240, "yield_strength": 60e6,
     "ultimate_strength": 70e6, "youngs_modulus": 3.5e9, "poisson": 0.36,
     "thermal_conductivity": 0.13, "specific_heat": 1800, "cost_per_kg": 2.5},
    {"name": "Carbon Fiber Composite", "density": 1600, "yield_strength": 600e6,
     "ultimate_strength": 600e6, "youngs_modulus": 70e9, "poisson": 0.30,
     "thermal_conductivity": 5.0, "specific_heat": 800, "cost_per_kg": 30.0},
    {"name": "Copper", "density": 8960, "yield_strength": 70e6,
     "ultimate_strength": 220e6, "youngs_modulus": 110e9, "poisson": 0.34,
     "thermal_conductivity": 401, "specific_heat": 385, "cost_per_kg": 8.0},
]


class MaterialDatabase:
    def __init__(self):
        self.materials = list(MATERIALS)

    def get(self, name: str) -> Dict[str, Any] | None:
        for m in self.materials:
            if m["name"].lower() == name.lower():
                return m
        return None

    def search(self, **filters) -> List[Dict[str, Any]]:
        results = self.materials
        for key, value in filters.items():
            results = [m for m in results if m.get(key) == value]
        return results

    def strongest(self, top: int = 3) -> List[Dict[str, Any]]:
        return sorted(self.materials,
                      key=lambda m: m["yield_strength"], reverse=True)[:top]

    def lightest(self, top: int = 3) -> List[Dict[str, Any]]:
        return sorted(self.materials, key=lambda m: m["density"])[:top]

    def add(self, material: Dict[str, Any]):
        self.materials.append(material)

    def all(self) -> List[Dict[str, Any]]:
        return list(self.materials)
