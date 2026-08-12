"""Assistant agent: provides actions based on the screen."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ai_models.reasoning_model import ReasoningModel
from ai_core.context_manager import ContextManager

logger = logging.getLogger(__name__)


class AssistantAgent:
    """Suggests and explains actions based on the current screen."""

    def __init__(self, reasoning_model: ReasoningModel | None = None,
                 context: ContextManager | None = None) -> None:
        self.reasoning = reasoning_model or ReasoningModel()
        self.context = context or ContextManager()

    def suggest(self, goal: str, screen_context: Dict[str, Any], image: Any = None) -> Dict[str, Any]:
        decision = self.reasoning.decide(goal, screen_context, image)
        self.context.set("last_suggestion", decision)
        return decision

    def plan(self, goal: str, screen_context: Dict[str, Any], image: Any = None) -> List[Dict[str, Any]]:
        from ai_core.reasoning_engine import ReasoningEngine
        return ReasoningEngine(self.reasoning.engine).plan_actions(goal, screen_context, image)

    def evaluate_risk(self, action: Dict[str, Any], screen_context: Dict[str, Any]) -> Dict[str, Any]:
        return self.reasoning.evaluate_risk(action, screen_context)

    def explain(self, observation: str) -> str:
        return self.reasoning.explain(observation)
