"""Understand screen structure and layout."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from ai_models.vision_model import VisionModel

logger = logging.getLogger(__name__)


class ScreenLayout:
    """Analyzes the structural layout of a screen."""

    def __init__(self, vision_model: VisionModel | None = None) -> None:
        self.vision_model = vision_model or VisionModel()

    def analyze(self, image: Any) -> Dict[str, Any]:
        return self.vision_model.describe_layout(image)

    def regions(self, image: Any) -> List[Dict[str, Any]]:
        layout = self.analyze(image)
        return layout.get("regions", [])

    def primary_focus(self, image: Any) -> str:
        layout = self.analyze(image)
        return layout.get("primary_focus", "")

    def grid_analysis(self, image: Any, rows: int = 3, cols: int = 3) -> List[List[str]]:
        """Describe the screen as a rows x cols grid of region descriptions."""
        raw = self.vision_model.engine.analyze_fast(
            f"Divide this screen into a {rows}x{cols} grid and describe each cell in 1-3 words. "
            "Return a JSON list of lists (rows) of strings. Respond with ONLY JSON.",
            image,
        )
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
            logger.debug("grid_analysis parse failed: %s", exc)
        return [["" for _ in range(cols)] for _ in range(rows)]
