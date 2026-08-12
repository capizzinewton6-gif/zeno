"""Google Gemini 1.5 Flash engine.

Responsible for fast document processing, literature parsing, metadata
extraction, information extraction, lightweight biological analysis,
validation tasks, context preparation, research preprocessing, and
supporting autonomous biological workflows.
"""
from __future__ import annotations

from ai_core.config_loader import get_api_key, load_settings
from ai_core.gemini_base import GeminiEngineBase


class Gemini15FlashEngine(GeminiEngineBase):
    """Secondary, lighter engine backed by Gemini 1.5 Flash."""

    MODEL_NAME = "gemini-1.5-flash"

    def __init__(self, api_key: str | None = None, **kwargs):
        settings = load_settings().get("ai_engine", {})
        super().__init__(
            api_key=api_key or get_api_key("google_api_key"),
            model=self.MODEL_NAME,
            temperature=kwargs.pop("temperature", 0.2),
            max_output_tokens=kwargs.pop("max_output_tokens", 4096),
            timeout=kwargs.pop("timeout_seconds", settings.get("timeout_seconds", 60)),
            **kwargs,
        )

    @property
    def role(self) -> str:
        return "fast preprocessing (Gemini 1.5 Flash)"


_ENGINE: Gemini15FlashEngine | None = None


def get_engine() -> Gemini15FlashEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = Gemini15FlashEngine()
    return _ENGINE
