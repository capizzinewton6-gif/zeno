"""Object analyzer: analyzes objects from image descriptions."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine


class ObjectAnalyzer:
    def __init__(self, engine: Gemini15FlashEngine | None = None):
        self.engine = engine or Gemini15FlashEngine()

    def analyze(self, description: str) -> str:
        return self.engine.generate(
            f"Analyze this object/image description and infer material, "
            f"dimensions, function, and condition: {description}",
            system="You are a computer vision analyst.")

    def classify(self, description: str) -> str:
        return self.engine.generate(
            f"Classify the object described: {description}. Give category and subtype.",
            system="You are an object classifier.")

    def defects(self, description: str) -> str:
        return self.engine.generate(
            f"Identify potential defects from this image description: {description}",
            system="You are a quality inspector.")
