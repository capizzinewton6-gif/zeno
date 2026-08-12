"""Google Gemini 1.5 Flash engine.

Responsible for fast symbolic preprocessing, formula extraction, document
parsing, metadata extraction, lightweight mathematical analysis, validation
tasks, context preparation, research preprocessing and supporting autonomous
mathematical workflows.
"""

from __future__ import annotations

from mathematics_ai.ai_core.engine_base import EngineConfig, GeminiEngineBase


class Gemini15FlashEngine(GeminiEngineBase):
    """Adapter for ``gemini-1.5-flash`` — the fast preprocessing engine."""

    model_name = "gemini-1.5-flash"
    role = "fast_preprocessing"

    def __init__(self, engine_config: EngineConfig | None = None) -> None:
        cfg = engine_config or EngineConfig(
            model=self.model_name,
            temperature=0.1,
            max_output_tokens=4096,
            role=self.role,
        )
        super().__init__(cfg)
