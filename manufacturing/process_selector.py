"""Process selector: chooses manufacturing processes."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine

# Process suitability by material and volume.
PROCESS_GUIDE = {
    "machining": {"materials": ["metal", "plastic"], "volume": "low-medium",
                  "tolerance": "high", "cost": "medium-high"},
    "injection_molding": {"materials": ["plastic"], "volume": "high",
                          "tolerance": "medium", "cost": "low per unit (high tooling)"},
    "casting": {"materials": ["metal"], "volume": "medium-high",
                "tolerance": "low-medium", "cost": "low-medium"},
    "3d_printing": {"materials": ["plastic", "metal"], "volume": "low",
                    "tolerance": "medium", "cost": "low setup, high per unit"},
    "sheet_metal": {"materials": ["metal"], "volume": "medium-high",
                    "tolerance": "medium", "cost": "low-medium"},
    "extrusion": {"materials": ["metal", "plastic"], "volume": "high",
                  "tolerance": "medium", "cost": "low"},
    "forging": {"materials": ["metal"], "volume": "high",
                "tolerance": "medium", "cost": "medium"},
}


class ProcessSelector:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.guide = PROCESS_GUIDE

    def select(self, part: str, material: str, volume: int) -> str:
        return self.engine.generate(
            f"Select manufacturing processes for {part} in {material} at "
            f"{volume} units. Justify with cost/quality trade-offs.",
            system="You are a process selection engineer.")

    def suitable(self, material_category: str, volume_label: str) -> list[str]:
        results = []
        for process, info in self.guide.items():
            if material_category.lower() in [m.lower() for m in info["materials"]]:
                if info["volume"].startswith(volume_label.lower().split("-")[0]):
                    results.append(process)
        return results

    def all_processes(self) -> dict:
        return dict(self.guide)
