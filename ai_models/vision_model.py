"""Screen understanding model backed by Gemini vision."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class VisionModel:
    """High-level screen understanding via Gemini 2.5 Flash."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def understand(self, image: Any, question: str = "What is shown on this screen?") -> str:
        return self.engine.reason(question, image)

    def describe_layout(self, image: Any) -> Dict[str, Any]:
        raw = self.engine.reason(
            "Describe the layout of this screen as JSON with keys: regions (list of "
            "{name, type, bbox}), primary_focus, and purpose. Respond with ONLY JSON.",
            image,
        )
        return self._safe_json(raw)

    def detect_changes(self, image_before: Any, image_after: Any) -> str:
        return self.engine.reason(
            "Compare these two screen images and describe what changed.", image_before
        )

    @staticmethod
    def _safe_json(raw: str) -> Dict[str, Any]:
        try:
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, dict) else {"result": data}
        except Exception:
            return {"raw": raw}
