"""Model router for Mathematics AI.

Routes requests between ``gemini-2.5-flash`` (advanced reasoning) and
``gemini-1.5-flash`` (fast preprocessing) based on a task classification.
Heavy/long-context reasoning tasks go to 2.5 Flash; lightweight preprocessing
and validation tasks go to 1.5 Flash. Both engines share the Gemini family;
no other model vendors are used.
"""

from __future__ import annotations

from typing import Any

from mathematics_ai.ai_core.engine_base import EngineResponse
from mathematics_ai.ai_core.gemini_15_flash_engine import Gemini15FlashEngine
from mathematics_ai.ai_core.gemini_25_flash_engine import Gemini25FlashEngine

FAST_KEYWORDS = (
    "preprocess", "preprocess", "parse", "extract", "metadata",
    "validate", "validation", "format", "classify", "normalise",
    "normalise", "summarise", "tokenise", "strip", "split",
)


class ModelRouter:
    """Selects the appropriate Gemini engine for a given task."""

    def __init__(self) -> None:
        self.advanced = Gemini25FlashEngine()
        self.fast = Gemini15FlashEngine()

    @property
    def engines(self) -> dict[str, Any]:
        return {"gemini-2.5-flash": self.advanced, "gemini-1.5-flash": self.fast}

    def classify(self, task: str) -> str:
        """Return ``"fast"`` for lightweight preprocessing tasks else ``"advanced"``."""
        lowered = task.lower()
        if any(kw in lowered for kw in FAST_KEYWORDS):
            return "fast"
        return "advanced"

    def route(self, task: str, prompt: str, **kwargs: Any) -> EngineResponse:
        """Classify ``task`` and dispatch ``prompt`` to the chosen engine."""
        if self.classify(task) == "fast":
            return self.fast.complete(prompt, **kwargs)
        return self.advanced.complete(prompt, **kwargs)

    def complete(self, prompt: str, engine: str = "auto", task: str = "", **kwargs: Any) -> EngineResponse:
        """Explicit completion API.

        ``engine`` may be ``"auto"`` (classify from ``task``), ``"advanced"``
        or ``"fast"``.
        """
        if engine == "auto":
            return self.route(task or prompt, prompt, **kwargs)
        if engine in {"advanced", "gemini-2.5-flash", "2.5"}:
            return self.advanced.complete(prompt, **kwargs)
        if engine in {"fast", "gemini-1.5-flash", "1.5"}:
            return self.fast.complete(prompt, **kwargs)
        raise ValueError(f"unknown engine: {engine!r}")
