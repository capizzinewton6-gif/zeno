"""Engineering knowledge engine: provides domain knowledge lookups and
knowledge-grounded generation via the primary Gemini engine."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class KnowledgeEngine:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def explain(self, topic: str) -> str:
        return self.engine.generate(
            f"Explain the engineering principles of: {topic}",
            system="You are an engineering knowledge base. Be rigorous and concise.")

    def formulas_for(self, topic: str) -> str:
        return self.engine.generate(
            f"List the key engineering formulas (with variable definitions) for: {topic}",
            system="Return formulas with SI units.")

    def standards_for(self, topic: str) -> str:
        return self.engine.generate(
            f"List relevant engineering standards (ISO, ASTM, IEC, ASME) for: {topic}",
            system="You are a standards reference.")

    def material_guidance(self, application: str) -> str:
        return self.engine.generate(
            f"Recommend suitable materials and justify for: {application}",
            system="You are a materials science expert.")

    def manufacturing_guidance(self, part: str) -> str:
        return self.engine.generate(
            f"Recommend manufacturing processes for: {part}",
            system="You are a manufacturing engineer.")
