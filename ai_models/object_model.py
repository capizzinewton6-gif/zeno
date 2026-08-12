"""Object detection model backed by Gemini vision."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class ObjectModel:
    """Detects and describes objects appearing on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def detect(self, image: Any, categories: List[str] | None = None) -> List[Dict[str, Any]]:
        cat_clause = f" Focus on: {', '.join(categories)}." if categories else ""
        raw = self.engine.reason(
            "Detect objects on this screen. Return a JSON list of objects, each with "
            "'name', 'bbox' [x,y,w,h] (normalized 0-1), and 'confidence'." + cat_clause +
            " Respond with ONLY the JSON list.",
            image,
        )
        return self._safe_list(raw)

    def count(self, image: Any, object_name: str) -> int:
        raw = self.engine.analyze_fast(
            f"Count how many '{object_name}' appear on this screen. Respond with only a number.",
            image,
        )
        try:
            return int("".join(ch for ch in raw if ch.isdigit()) or "0")
        except Exception:
            return 0

    def classify(self, image: Any) -> str:
        return self.engine.analyze_fast(
            "Classify the primary content type of this screen (e.g. 'text editor', "
            "'browser', 'game', 'dialog'). Respond with only the label.",
            image,
        )

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
            return [{"raw": raw}]
