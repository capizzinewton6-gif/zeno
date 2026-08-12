"""3D printing preparation: slicer settings and printability analysis."""

from __future__ import annotations

import math

from src.gemini_25_flash_engine import Gemini25FlashEngine


class Printing3D:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def slicer_settings(self, material: str, part: str) -> str:
        return self.engine.generate(
            f"Recommend slicer settings (layer height, infill, supports, speeds, "
            f"temperatures) for {material} part: {part}.",
            system="You are an additive manufacturing engineer.")

    def printability(self, geometry: str) -> str:
        return self.engine.generate(
            f"Analyse printability (overhangs, bridges, warping, supports) for: {geometry}.",
            system="You are a DFM engineer for 3D printing.")

    def material_estimate(self, volume_mm3: float, density_g_cm3: float,
                          infill: float = 0.2) -> dict:
        effective_volume = volume_mm3 * (0.2 + 0.8 * infill)  # shell + infill approx
        mass_g = effective_volume * density_g_cm3 / 1000  # mm3->cm3
        return {"effective_volume_mm3": effective_volume,
                "mass_g": mass_g, "infill": infill}

    def print_time_estimate(self, volume_mm3: float, layer_height: float = 0.2,
                            print_speed: float = 50.0) -> float:
        """Rough estimate (hours) based on volumetric flow."""
        flow = print_speed * 0.4 * layer_height  # mm3/s approx (0.4 nozzle)
        return volume_mm3 / flow / 3600 if flow > 0 else float("inf")
