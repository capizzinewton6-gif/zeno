"""Understand situations through Gemini reasoning."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Wraps Gemini 2.5 Flash for multi-step reasoning and situational understanding."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def analyze_situation(self, context: Dict[str, Any], image: Any = None) -> str:
        prompt = (
            "Analyze the following screen situation and explain what is happening, "
            "what the user is likely trying to do, and any risks.\n\n"
            f"Context: {json.dumps(context, default=str)[:2000]}"
        )
        return self.engine.reason(prompt, image)

    def plan_actions(self, goal: str, context: Dict[str, Any], image: Any = None) -> List[Dict[str, Any]]:
        prompt = (
            "You are planning screen automation actions to achieve a goal. "
            "Return a JSON list of steps. Each step has 'action' (click/type/wait/scroll/key), "
            "'target', and 'description'.\n\n"
            f"Goal: {goal}\n"
            f"Context: {json.dumps(context, default=str)[:2000]}\n\n"
            "Respond with ONLY the JSON list."
        )
        raw = self.engine.reason(prompt, image)
        return self._parse_steps(raw)

    def security_analysis(self, action: str, context: Dict[str, Any]) -> str:
        prompt = (
            "Perform a security analysis of the proposed screen automation action. "
            "Identify risks and recommend safeguards.\n\n"
            f"Action: {action}\n"
            f"Context: {json.dumps(context, default=str)[:1500]}"
        )
        return self.engine.reason(prompt)

    def _parse_steps(self, raw: str) -> List[Dict[str, Any]]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception as exc:
            logger.warning("Failed to parse action plan: %s", exc)
        return [{"action": "none", "description": raw[:200]}]
