"""Understand websites."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class WebpageAnalyzer:
    """Understands the content of a web page shown on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def analyze(self, image: Any) -> Dict[str, Any]:
        raw = self.engine.reason(
            "Analyze this web page. Return JSON with keys: 'url_guess', 'page_type' "
            "(search/homepage/article/shop/login/dashboard/other), 'main_content', "
            "'navigation' (list), 'forms' (list of {'purpose','fields'}), and 'actions_available' (list). "
            "Respond with ONLY JSON.",
            image,
        )
        return self._safe_json(raw)

    def summarize(self, image: Any) -> str:
        data = self.analyze(image)
        return data.get("main_content", str(data))

    def is_login_page(self, image: Any) -> bool:
        data = self.analyze(image)
        return data.get("page_type") == "login" or bool(data.get("forms"))

    def extract_links(self, image: Any) -> list:
        return self.analyze(image).get("navigation", [])

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
