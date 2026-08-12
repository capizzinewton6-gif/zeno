"""Central AI engine that coordinates the Gemini 2.5 Flash (primary) and
Gemini 1.5 Flash (secondary) engines and exposes a unified intelligence API
to the invention capability modules."""

from __future__ import annotations

import logging
import os
from typing import List, Optional

from src.gemini_25_flash_engine import Gemini25FlashEngine
from src.gemini_15_flash_engine import Gemini15FlashEngine

logger = logging.getLogger(__name__)


class AIEngine:
    """Routes requests to the appropriate Gemini engine.

    ``primary`` (Gemini 2.5 Flash) handles deep reasoning, planning, and
    concept generation. ``secondary`` (Gemini 1.5 Flash) handles fast
    extraction, parsing, validation, and preprocessing.
    """

    def __init__(self, primary: Optional[Gemini25FlashEngine] = None,
                 secondary: Optional[Gemini15FlashEngine] = None):
        self.primary = primary or Gemini25FlashEngine()
        self.secondary = secondary or Gemini15FlashEngine()

    @property
    def models(self) -> List[dict]:
        """Lightweight model descriptors for the UI."""
        return [
            {"name": self.primary.display_name, "id": self.primary.model_name,
             "role": "primary", "online": self.primary.is_online,
             "responsibilities": self.primary.responsibilities},
            {"name": self.secondary.display_name, "id": self.secondary.model_name,
             "role": "secondary", "online": self.secondary.is_online,
             "responsibilities": self.secondary.responsibilities},
        ]

    def reason(self, prompt: str, system: Optional[str] = None) -> str:
        return self.primary.generate(prompt, system=system)

    def fast(self, prompt: str, system: Optional[str] = None) -> str:
        return self.secondary.generate(prompt, system=system)

    def extract_metadata(self, text: str) -> dict:
        return self.secondary.extract_metadata(text)

    def parse_patent(self, text: str) -> dict:
        return self.secondary.parse_patent(text)

    def validate(self, claim: str) -> str:
        return self.secondary.validate(claim)


def load_prompt() -> str:
    path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(path, encoding="utf-8") as f:
        return f.read()


ai_engine = AIEngine()
