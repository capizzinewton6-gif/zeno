"""Anti-spoofing / liveness detection: blink, texture, depth."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class LivenessResult:
    is_live: bool
    score: float
    reasons: List[str]


class AntiSpoofing:
    """Heuristic liveness checks usable without a deep anti-spoof model."""

    def __init__(self, blink_threshold: float = 0.20,
                 texture_min: float = 8.0) -> None:
        self.blink_threshold = blink_threshold
        self.texture_min = texture_min
        self._ear_history: List[float] = []

    def check(self, face_image: np.ndarray, ear: float = 0.30) -> LivenessResult:
        reasons: List[str] = []
        score = 0.0

        texture = self._laplacian_variance(face_image)
        if texture >= self.texture_min:
            score += 0.4
            reasons.append(f"texture_ok({texture:.1f})")
        else:
            reasons.append(f"texture_low({texture:.1f})")

        self._ear_history.append(ear)
        if len(self._ear_history) > 30:
            self._ear_history = self._ear_history[-30:]
        if len(self._ear_history) >= 6 and min(self._ear_history) < self.blink_threshold:
            score += 0.4
            reasons.append("blink_detected")
        elif len(self._ear_history) >= 6:
            reasons.append("no_blink")

        # Simple color-channels consistency (screenshots often have flat gradients)
        if face_image.ndim == 3 and self._channel_variance(face_image) > 5:
            score += 0.2
            reasons.append("color_variance_ok")

        return LivenessResult(is_live=score >= 0.6, score=score, reasons=reasons)

    @staticmethod
    def _laplacian_variance(image: np.ndarray) -> float:
        try:
            import cv2  # type: ignore
            gray = image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return float(cv2.Laplacian(gray, cv2.CV_64F).var())
        except Exception:
            return float(np.var(image))

    @staticmethod
    def _channel_variance(image: np.ndarray) -> float:
        if image.ndim != 3:
            return 0.0
        return float(np.mean([np.var(image[:, :, c]) for c in range(image.shape[2])]))
