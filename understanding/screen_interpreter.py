"""Understand what is displayed on screen."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from ai_core.ai_engine import get_engine
from recognition.screen_layout import ScreenLayout
from recognition.window_detector import WindowDetector

logger = logging.getLogger(__name__)


class ScreenInterpreter:
    """High-level interpretation of the current screen state."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()
        self.layout = ScreenLayout()
        self.windows = WindowDetector()

    def interpret(self, image: Any) -> Dict[str, Any]:
        layout = self.layout.analyze(image)
        active = self.windows.active_window()
        raw = self.engine.reason(
            "Interpret the overall meaning of this screen. Return JSON with keys: "
            "'summary', 'intent' (what the user is doing), 'context_type' "
            "(e.g. browsing/editing/reading/dialog), 'key_elements' (list). "
            "Respond with ONLY JSON.",
            image,
        )
        interpretation = self._safe_json(raw)
        interpretation["layout"] = layout
        interpretation["active_window"] = active
        return interpretation

    def summarize(self, image: Any) -> str:
        data = self.interpret(image)
        return data.get("summary", str(data))

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
