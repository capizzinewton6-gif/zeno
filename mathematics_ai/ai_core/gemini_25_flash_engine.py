"""Google Gemini 2.5 Flash engine.

Responsible for advanced mathematical reasoning, multi-step proof construction,
theorem exploration, complex derivations, research-level analysis, long-context
mathematical reasoning, mathematical decision making, autonomous theorem-based
reasoning and mathematical workflow orchestration.
"""

from __future__ import annotations

from mathematics_ai.ai_core.engine_base import EngineConfig, GeminiEngineBase


class Gemini25FlashEngine(GeminiEngineBase):
    """Adapter for ``gemini-2.5-flash`` — the primary reasoning engine."""

    model_name = "gemini-2.5-flash"
    role = "advanced_reasoning"

    def __init__(self, engine_config: EngineConfig | None = None) -> None:
        cfg = engine_config or EngineConfig(
            model=self.model_name,
            temperature=0.2,
            max_output_tokens=8192,
            role=self.role,
        )
        super().__init__(cfg)
