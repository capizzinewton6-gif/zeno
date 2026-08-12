"""Blueprint reader: interprets engineering drawings from descriptions."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class BlueprintReader:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def read(self, drawing_description: str) -> str:
        return self.engine.generate(
            f"Interpret this engineering drawing: views, dimensions, tolerances, "
            f"GD&T, annotations:\n{drawing_description}",
            system="You are a drafting interpreter.")

    def extract_dimensions(self, drawing_description: str) -> str:
        return self.engine.generate(
            f"Extract all dimensions and tolerances as a table from: {drawing_description}",
            system="You are a dimension extractor.")

    def identify_views(self, drawing_description: str) -> str:
        return self.engine.generate(
            f"Identify the views present (front, top, side, section, isometric) in: "
            f"{drawing_description}",
            system="You are a drawing analyst.")
