"""Paper reader: parses and summarizes technical papers (via fast engine)."""

from __future__ import annotations

from src.gemini_15_flash_engine import Gemini15FlashEngine
from src.gemini_25_flash_engine import Gemini25FlashEngine


class PaperReader:
    def __init__(self, fast_engine: Gemini15FlashEngine | None = None,
                 deep_engine: Gemini25FlashEngine | None = None):
        self.fast = fast_engine or Gemini15FlashEngine()
        self.deep = deep_engine or Gemini25FlashEngine()

    def summarize(self, text: str) -> str:
        return self.fast.generate(
            f"Summarize this technical paper (abstract, methods, results, "
            f"conclusions):\n{text}",
            system="You are a scientific summarizer.")

    def extract_metadata(self, text: str) -> str:
        return self.fast.generate(
            f"Extract metadata (title, authors, year, venue, DOI) from:\n{text}",
            system="You are a metadata extractor.")

    def critique(self, text: str) -> str:
        return self.deep.generate(
            f"Critically review this paper (methodology, validity, limitations, "
            f"relevance):\n{text}",
            system="You are a peer reviewer.")

    def extract_references(self, text: str) -> str:
        return self.fast.generate(
            f"Extract the reference list (authors, title, year, venue) from:\n{text}",
            system="You are a reference extractor.")
