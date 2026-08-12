"""Common base class for all agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai_core.safety_layer import SafetyLayer
from modeling.neural_backbones import NeuralBackbone, get_backbone


@dataclass
class AgentResult:
    agent: str
    capability: str
    content: str
    actions: list[str] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "capability": self.capability,
            "actions": self.actions,
            "artifacts": self.artifacts,
            "error": self.error,
        }


class BaseAgent:
    """Base for all CODING_AI agents."""

    name: str = "base"
    capability: str = "code_synthesis"

    def __init__(self, backbone: NeuralBackbone | None = None,
                 safety: SafetyLayer | None = None,
                 workspace: str = ".") -> None:
        self.backbone = backbone or get_backbone()
        self.safety = safety or SafetyLayer()
        self.workspace = workspace

    def run(self, message: str, **kwargs: Any) -> dict[str, Any]:
        """Execute the agent. Subclasses override ``_execute``."""
        try:
            result = self._execute(message, **kwargs)
            return result.to_dict() if isinstance(result, AgentResult) else result
        except Exception as exc:
            return AgentResult(self.name, self.capability, "",
                               error=str(exc)).to_dict()

    def _execute(self, message: str, **kwargs: Any) -> AgentResult:
        raise NotImplementedError
