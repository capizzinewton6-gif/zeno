"""Scene classifier: indoor/outdoor, night, crowded, etc."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class SceneInfo:
    scene_type: str
    lighting: str
    time_of_day: str
    crowdedness: str
    summary: str
    confidence: float = 0.0


class SceneClassifier:
    """Classify scene context. Local brightness heuristic + Gemini fallback."""

    def __init__(self, flash25=None) -> None:
        self._flash25 = flash25

    def classify(self, image: np.ndarray) -> SceneInfo:
        info = self._local(image)
        if info is not None:
            return info
        return self._gemini(image)

    def _local(self, image: np.ndarray) -> Optional[SceneInfo]:
        if image is None or image.size == 0:
            return SceneInfo("unknown", "unknown", "unknown", "unknown", "no image", 0.0)
        gray = image.mean(axis=2) if image.ndim == 3 else image
        mean = float(gray.mean())
        std = float(gray.std())
        lighting = "dark" if mean < 60 else ("bright" if mean > 180 else "normal")
        time_of_day = "night" if mean < 70 else "day"
        crowdedness = "sparse" if std < 30 else "moderate"
        return SceneInfo("unknown", lighting, time_of_day, crowdedness,
                         f"local: brightness={mean:.0f}, contrast={std:.0f}", 0.4)

    def _gemini(self, image: np.ndarray) -> SceneInfo:
        if self._flash25 is None:
            from src.gemini_25_flash_engine import Gemini25FlashEngine
            self._flash25 = Gemini25FlashEngine()
        from core_vision.frame_preprocessor import FramePreprocessor
        jpeg = FramePreprocessor().to_jpeg_bytes(image, 85)
        if not jpeg:
            return self._local(image)
        result = self._flash25.describe_scene(jpeg)
        if isinstance(result, dict) and "scene_type" in result:
            return SceneInfo(
                scene_type=str(result.get("scene_type", "unknown")),
                lighting=str(result.get("lighting", "unknown")),
                time_of_day=str(result.get("time_of_day", "unknown")),
                crowdedness=str(result.get("crowdedness", "unknown")),
                summary=str(result.get("summary", "")), confidence=0.8)
        return self._local(image)
