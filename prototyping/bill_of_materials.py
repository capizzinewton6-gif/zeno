"""Bill of materials generation."""

from __future__ import annotations

import csv
import os
from typing import List

from src.gemini_25_flash_engine import Gemini25FlashEngine


class BillOfMaterials:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()
        self.items: List[dict] = []

    def add(self, part_number: str, description: str, quantity: int,
            unit_cost: float = 0.0, supplier: str = ""):
        self.items.append({
            "part_number": part_number, "description": description,
            "quantity": quantity, "unit_cost": unit_cost,
            "supplier": supplier,
            "total_cost": round(quantity * unit_cost, 2),
        })

    def total_cost(self) -> float:
        return round(sum(i["total_cost"] for i in self.items), 2)

    def generate(self, concept: str) -> str:
        return self.engine.generate(
            f"Generate a bill of materials (part, description, qty, unit cost, "
            f"supplier) for: {concept}. Return as a table.",
            system="You are a procurement engineer.")

    def to_csv(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["part_number", "description",
                                                   "quantity", "unit_cost",
                                                   "total_cost", "supplier"])
            writer.writeheader()
            writer.writerows(self.items)
        return path
