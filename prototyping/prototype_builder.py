"""Prototype builder: plans prototype construction."""

from __future__ import annotations

from src.gemini_25_flash_engine import Gemini25FlashEngine


class PrototypeBuilder:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def plan(self, concept: str) -> str:
        return self.engine.generate(
            f"Create a prototype build plan (materials, methods, sequence, risks) for: {concept}",
            system="You are a prototyping engineer.")

    def iterate(self, prototype: str, feedback: str) -> str:
        return self.engine.generate(
            f"Given prototype:\n{prototype}\nand test feedback:\n{feedback}\n"
            f"Produce an iteration plan.",
            system="You are a prototype iteration engineer.")

    def define_success(self, concept: str) -> str:
        return self.engine.generate(
            f"Define prototype success criteria and metrics for: {concept}",
            system="You are a test engineer.")
