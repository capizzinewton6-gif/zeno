"""Detect buttons, menus, icons, and other UI elements."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ai_models.ui_model import UIModel

logger = logging.getLogger(__name__)


class UIElementDetector:
    """Detects interactive UI elements on screen.

    Combines classical computer-vision heuristics (when OpenCV is available)
    with the Gemini-backed UIModel for semantic understanding.
    """

    def __init__(self, ui_model: UIModel | None = None) -> None:
        self.ui_model = ui_model or UIModel()

    def detect(self, image: Any) -> List[Dict[str, Any]]:
        elements = self.ui_model.detect_elements(image)
        cv_elements = self._cv_detect(image)
        return self._merge(elements, cv_elements)

    def detect_by_type(self, image: Any, element_type: str) -> List[Dict[str, Any]]:
        all_elements = self.detect(image)
        low = element_type.lower()
        return [e for e in all_elements if low in str(e.get("type", "")).lower()]

    def _cv_detect(self, image: Any) -> List[Dict[str, Any]]:
        try:
            import cv2  # type: ignore
            import numpy as np  # type: ignore
            arr = self._to_array(image)
            if arr is None:
                return []
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            results = []
            h, w = gray.shape
            for c in contours:
                x, y, cw, ch = cv2.boundingRect(c)
                if cw * ch < 100 or cw > w * 0.9:
                    continue
                results.append({
                    "type": "region",
                    "text": "",
                    "bbox": [x / w, y / h, cw / w, ch / h],
                    "confidence": 0.5,
                    "source": "cv",
                })
            return results
        except Exception as exc:
            logger.debug("CV UI detection skipped: %s", exc)
            return []

    @staticmethod
    def _to_array(image: Any):
        try:
            import numpy as np  # type: ignore
            from PIL import Image  # type: ignore
            if isinstance(image, str):
                return np.array(Image.open(image))
            if isinstance(image, (bytes, bytearray)):
                import io
                return np.array(Image.open(io.BytesIO(image)))
            if hasattr(image, "rgb") and hasattr(image, "size"):
                arr = np.frombuffer(image.rgb, dtype=np.uint8)
                return arr.reshape((image.size[1], image.size[0], 3))
            if isinstance(image, Image.Image):
                return np.array(image)
        except Exception as exc:
            logger.debug("_to_array failed: %s", exc)
        return None

    @staticmethod
    def _merge(a: List[Dict[str, Any]], b: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        merged = []
        for el in a + b:
            key = (el.get("type"), tuple(el.get("bbox", [])))
            if key in seen:
                continue
            seen.add(key)
            merged.append(el)
        return merged
