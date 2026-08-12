"""Identify icons on screen."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ai_core.ai_engine import get_engine

logger = logging.getLogger(__name__)


class IconRecognition:
    """Recognizes and labels icons appearing on screen."""

    def __init__(self, engine=None) -> None:
        self.engine = engine or get_engine()

    def identify(self, image: Any) -> List[Dict[str, Any]]:
        raw = self.engine.analyze_fast(
            "Identify all icons visible on this screen. Return a JSON list with 'name', "
            "'bbox' [x,y,w,h] normalized 0-1, and 'confidence'. Respond with ONLY the JSON list.",
            image,
        )
        try:
            import json
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.lower().startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def describe_icon(self, image: Any, region: tuple[int, int, int, int]) -> str:
        try:
            from PIL import Image  # type: ignore
            import io
            if isinstance(image, str):
                img = Image.open(image)
            elif isinstance(image, (bytes, bytearray)):
                img = Image.open(io.BytesIO(image))
            else:
                img = image
            x, y, w, h = region
            cropped = img.crop((x, y, x + w, y + h))
            return self.engine.analyze_fast(
                "What icon is shown here? Respond with the icon's name and meaning in one sentence.",
                cropped,
            )
        except Exception as exc:
            logger.warning("describe_icon failed: %s", exc)
            return self.engine.analyze_fast("Describe the icon shown.", image)
