"""Patent search and analysis via engine."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine
from src.gemini_25_flash_engine import Gemini25FlashEngine


class PatentSearch:
    def __init__(self, fast_engine: Gemini15FlashEngine | None = None,
                 deep_engine: Gemini25FlashEngine | None = None):
        self.fast = fast_engine or Gemini15FlashEngine()
        self.deep = deep_engine or Gemini25FlashEngine()

    def search(self, concept: str) -> str:
        return self.fast.generate(
            f"Generate likely patent keywords and classification (IPC/CPC) codes "
            f"for concept: {concept}.",
            system="You are a patent search analyst.")

    def novelty(self, concept: str, prior_art: str = "") -> str:
        return self.deep.generate(
            f"Assess novelty of: {concept}. Prior art: {prior_art}. "
            f"Identify distinguishing features.",
            system="You are a patent analyst.")

    def claims_outline(self, concept: str) -> str:
        return self.deep.generate(
            f"Draft an outline of independent and dependent patent claims for: {concept}.",
            system="You are a patent attorney.")

    def classify(self, concept: str) -> str:
        return self.fast.generate(
            f"Propose IPC/CPC classification for: {concept}",
            system="You are a patent classifier.")
