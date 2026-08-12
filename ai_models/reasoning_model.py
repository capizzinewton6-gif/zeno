"""Decision-making model backed by Gemini 2.5 Flash reasoning."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class ReasoningModel:
    """Makes decisions about what to do given a screen context."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def decide(self, goal: str, context: Dict[str, Any], image: Any = None) -> Dict[str, Any]:
        raw = self.engine.reason(
            "You are deciding the next action to achieve a goal on a screen. "
            "Return JSON with 'decision', 'action' (click/type/scroll/wait/none), "
            "'target', 'coordinates' [x,y] normalized 0-1, 'confidence' 0-1, 'reasoning'.\n\n"
            f"Goal: {goal}\nContext: {json.dumps(context, default=str)[:1500]}\n"
            "Respond with ONLY JSON.",
            image,
        )
        return self._safe_dict(raw)

    def evaluate_risk(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        raw = self.engine.reason(
            "Evaluate the risk of performing this screen action. Return JSON with "
            "'risk_level' (low/medium/high), 'concerns' (list), 'mitigations' (list).\n\n"
            f"Action: {json.dumps(action, default=str)}\n"
            f"Context: {json.dumps(context, default=str)[:1000]}\n"
            "Respond with ONLY JSON.",
        )
        return self._safe_dict(raw)

    def explain(self, observation: str) -> str:
        return self.engine.reason(f"Explain this screen observation in plain language: {observation}")

    @staticmethod
    def _safe_dict(raw: str) -> Dict[str, Any]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {"raw": raw}
