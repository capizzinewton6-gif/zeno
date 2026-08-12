"""Analyze games and interactive interfaces."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class GameAnalyzer:
    """Understands game states and interactive interfaces."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def analyze(self, image: Any) -> Dict[str, Any]:
        raw = self.engine.reason(
            "Analyze this game or interactive interface. Return JSON with keys: "
            "'is_game' (bool), 'game_title', 'genre', 'current_state', 'score_visible', "
            "'hud_elements' (list), 'next_action' (suggested), and 'difficulty'. "
            "Respond with ONLY JSON.",
            image,
        )
        return self._safe_json(raw)

    def is_game(self, image: Any) -> bool:
        return bool(self.analyze(image).get("is_game", False))

    def suggest_move(self, image: Any) -> str:
        return self.analyze(image).get("next_action", "")

    @staticmethod
    def _safe_json(raw: str) -> Dict[str, Any]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, dict) else {"raw": data}
        except Exception:
            return {"raw": raw}
