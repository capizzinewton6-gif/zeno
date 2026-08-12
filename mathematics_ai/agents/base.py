"""Base classes shared by all agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mathematics_ai.ai_core import Gemini25FlashEngine, Gemini15FlashEngine, ModelRouter


@dataclass
class AgentResult:
    """Standard result returned by every agent."""

    agent: str
    success: bool
    answer: Any = None
    steps: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "success": self.success,
            "answer": self.answer,
            "steps": self.steps,
            "metadata": self.metadata,
            "error": self.error,
        }


class BaseAgent:
    """Common agent scaffolding: engine access and result helpers."""

    name: str = "base_agent"

    def __init__(self) -> None:
        self.advanced = Gemini25FlashEngine()
        self.fast = Gemini15FlashEngine()
        self.router = ModelRouter()

    def result(self, answer: Any, steps: list[dict[str, Any]] | None = None, success: bool = True, **meta: Any) -> AgentResult:
        return AgentResult(agent=self.name, success=success, answer=answer, steps=steps or [], metadata=meta)

    def fail(self, error: str, **meta: Any) -> AgentResult:
        return AgentResult(agent=self.name, success=False, error=error, metadata=meta)
