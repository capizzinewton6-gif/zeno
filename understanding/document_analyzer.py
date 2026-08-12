"""Understand documents."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """Understands documents displayed on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def analyze(self, image: Any) -> Dict[str, Any]:
        raw = self.engine.reason(
            "Analyze this document. Return JSON with keys: 'doc_type' "
            "(pdf/word/spreadsheet/code/presentation/email/other), 'title', 'summary', "
            "'key_points' (list), 'action_items' (list), and 'language'. "
            "Respond with ONLY JSON.",
            image,
        )
        return self._safe_json(raw)

    def summarize(self, image: Any) -> str:
        return self.analyze(image).get("summary", "")

    def extract_action_items(self, image: Any) -> list:
        return self.analyze(image).get("action_items", [])

    def type(self, image: Any) -> str:
        return self.analyze(image).get("doc_type", "other")

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
