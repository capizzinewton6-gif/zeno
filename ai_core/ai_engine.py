"""Main AI intelligence hub that routes between Gemini engines and biological modules."""
from __future__ import annotations

from typing import Any

from src.gemini_25_flash_engine.engine import get_engine as get_primary
from src.gemini_15_flash_engine.engine import get_engine as get_secondary
from ai_core.gemini_base import load_system_prompt


class AIEngine:
    """Coordinates the primary (2.5 Flash) and secondary (1.5 Flash) engines."""

    def __init__(self):
        self.primary = get_primary()
        self.secondary = get_secondary()
        self.system_prompt = load_system_prompt()

    @property
    def available(self) -> bool:
        return self.primary.available or self.secondary.available

    def reason(self, prompt: str, use_secondary: bool = False) -> str:
        """High-level biological reasoning via the appropriate Gemini engine."""
        engine = self.secondary if use_secondary else self.primary
        return engine.generate(prompt, system=self.system_prompt)

    def fast_parse(self, text: str) -> str:
        """Lightweight document / metadata extraction via 1.5 Flash."""
        return self.secondary.generate(
            "Extract the key biological facts, entities, and numeric data from the "
            "following text as concise bullet points:\n\n" + text,
            system=self.system_prompt,
        )

    def status(self) -> dict[str, Any]:
        return {
            "primary_engine": {
                "model": self.primary.model,
                "role": self.primary.role,
                "available": self.primary.available,
            },
            "secondary_engine": {
                "model": self.secondary.model,
                "role": self.secondary.role,
                "available": self.secondary.available,
            },
            "system_prompt_loaded": bool(self.system_prompt),
        }
