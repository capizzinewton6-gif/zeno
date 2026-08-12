"""Interface understanding model backed by Gemini."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class UIModel:
    """Understands user-interface semantics on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def detect_elements(self, image: Any) -> List[Dict[str, Any]]:
        raw = self.engine.reason(
            "Detect all interactive UI elements on this screen (buttons, links, "
            "menus, inputs, checkboxes, toggles, dropdowns). Return a JSON list with "
            "'type', 'text', 'bbox' [x,y,w,h] (normalized 0-1), 'state', and 'action_hint'. "
            "Respond with ONLY the JSON list.",
            image,
        )
        return self._safe_list(raw)

    def find_element(self, image: Any, description: str) -> Dict[str, Any] | None:
        raw = self.engine.reason(
            f"Find the UI element matching this description: '{description}'. "
            "Return JSON with 'type', 'text', 'bbox' [x,y,w,h] normalized 0-1, 'state'. "
            "If not found, return {\"found\": false}. Respond with ONLY JSON.",
            image,
        )
        data = self._safe_dict(raw)
        if data.get("found") is False:
            return None
        return data or None

    def suggest_action(self, image: Any, goal: str) -> Dict[str, Any]:
        raw = self.engine.reason(
            f"Goal: {goal}. Suggest the single next UI action on this screen. "
            "Return JSON with 'element', 'action', 'bbox', 'rationale'. "
            "Respond with ONLY JSON.",
            image,
        )
        return self._safe_dict(raw)

    @staticmethod
    def _safe_list(raw: str) -> List[Dict[str, Any]]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, list) else []
        except Exception:
            return []

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
