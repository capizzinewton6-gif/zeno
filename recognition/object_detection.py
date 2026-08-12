"""Detect objects on screen."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ai_models.object_model import ObjectModel

logger = logging.getLogger(__name__)


class ObjectDetection:
    """Detects and describes objects appearing on screen."""

    def __init__(self, object_model: ObjectModel | None = None) -> None:
        self.object_model = object_model or ObjectModel()

    def detect(self, image: Any, categories: List[str] | None = None) -> List[Dict[str, Any]]:
        return self.object_model.detect(image, categories)

    def count(self, image: Any, object_name: str) -> int:
        return self.object_model.count(image, object_name)

    def classify_scene(self, image: Any) -> str:
        return self.object_model.classify(image)

    def locate(self, image: Any, object_name: str) -> Dict[str, Any] | None:
        for obj in self.detect(image):
            if object_name.lower() in str(obj.get("name", "")).lower():
                return obj
        return None
