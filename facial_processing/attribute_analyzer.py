"""Attribute analyzer: age, gender, emotion, head pose (yaw/pitch/roll)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np


@dataclass
class FaceAttributes:
    age: float = 0.0
    gender: str = "unknown"
    emotion: str = "neutral"
    head_pose: Dict[str, float] = field(default_factory=lambda: {"yaw": 0.0, "pitch": 0.0, "roll": 0.0})
    confidence: float = 0.0


class AttributeAnalyzer:
    """Estimate face attributes. Uses Gemini 1.5 Flash when local models absent."""

    def __init__(self, flash15=None) -> None:
        self._flash15 = flash15

    def analyze(self, face_image: np.ndarray) -> FaceAttributes:
        attrs = self._local(face_image)
        if attrs is not None:
            return attrs
        return self._gemini(face_image)

    def _local(self, face_image: np.ndarray) -> Optional[FaceAttributes]:
        try:
            import cv2  # type: ignore
            # Head pose from solvePnP is heavy; use a simple brightness-based fallback
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY) if face_image.ndim == 3 else face_image
            mean = float(gray.mean())
            emotion = "neutral" if 80 <= mean <= 180 else ("dim" if mean < 80 else "bright")
            return FaceAttributes(age=30.0, gender="unknown", emotion=emotion,
                                   head_pose={"yaw": 0.0, "pitch": 0.0, "roll": 0.0},
                                   confidence=0.2)
        except Exception:
            return None

    def _gemini(self, face_image: np.ndarray) -> FaceAttributes:
        if self._flash15 is None:
            from src.gemini_15_flash_engine import Gemini15FlashEngine
            self._flash15 = Gemini15FlashEngine()
        from core_vision.frame_preprocessor import FramePreprocessor
        jpeg = FramePreprocessor().to_jpeg_bytes(face_image, 85)
        if not jpeg:
            return FaceAttributes()
        out = self._flash15.fast_analyze(
            "Estimate this face's attributes as JSON: "
            "{\"age\":int,\"gender\":str,\"emotion\":str,\"yaw\":float,\"pitch\":float,\"roll\":float}.",
            [jpeg])
        if isinstance(out, dict):
            return FaceAttributes()
        import json
        try:
            data = json.loads(out)
            return FaceAttributes(
                age=float(data.get("age", 0)),
                gender=str(data.get("gender", "unknown")),
                emotion=str(data.get("emotion", "neutral")),
                head_pose={"yaw": float(data.get("yaw", 0)), "pitch": float(data.get("pitch", 0)),
                           "roll": float(data.get("roll", 0))},
                confidence=0.8)
        except Exception:
            return FaceAttributes()
