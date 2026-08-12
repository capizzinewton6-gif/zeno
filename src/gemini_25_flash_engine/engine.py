"""Google Gemini 2.5 Flash engine.

Responsible for advanced biological reasoning, multi-step scientific planning,
experimental interpretation, hypothesis generation, research-level analysis,
long-context biological reasoning, scientific decision making, biological
workflow orchestration, and complex systems analysis.
"""
from __future__ import annotations

from pathlib import Path

from ai_core.config_loader import get_api_key, load_settings
from ai_core.gemini_base import GeminiEngineBase


class Gemini25FlashEngine(GeminiEngineBase):
    """Primary reasoning engine backed by Gemini 2.5 Flash."""

    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self, api_key: str | None = None, **kwargs):
        settings = load_settings().get("ai_engine", {})
        super().__init__(
            api_key=api_key or get_api_key("google_api_key"),
            model=self.MODEL_NAME,
            temperature=kwargs.pop("temperature", settings.get("temperature", 0.4)),
            max_output_tokens=kwargs.pop(
                "max_output_tokens", settings.get("max_output_tokens", 8192)
            ),
            timeout=kwargs.pop("timeout_seconds", settings.get("timeout_seconds", 60)),
            **kwargs,
        )

    @property
    def role(self) -> str:
        return "primary reasoning (Gemini 2.5 Flash)"


_ENGINE: Gemini25FlashEngine | None = None


def get_engine() -> Gemini25FlashEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = Gemini25FlashEngine()
    return _ENGINE
