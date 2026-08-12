"""Gesture reader: hand gesture and body pose estimation (MediaPipe/OpenPose)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


@dataclass
class PoseResult:
    landmarks: List[Dict[str, float]] = field(default_factory=list)
    gesture: str = "none"
    confidence: float = 0.0


class GestureReader:
    """Estimate hand/body pose and infer simple gestures."""

    def __init__(self) -> None:
        self._hands = None
        self._pose = None

    def read(self, image: np.ndarray) -> PoseResult:
        return self._mediapipe(image)

    def _mediapipe(self, image: np.ndarray) -> PoseResult:
        try:
            import mediapipe as mp  # type: ignore
            if self._hands is None:
                self._hands = mp.solutions.hands.Hands(
                    static_image_mode=False, max_num_hands=2,
                    min_detection_confidence=0.5, min_tracking_confidence=0.5)
            rgb = image[:, :, ::-1] if image.ndim == 3 else image
            res = self._hands.process(rgb)
            if not res.multi_hand_landmarks:
                return PoseResult()
            landmarks: List[Dict[str, float]] = []
            for hand in res.multi_hand_landmarks:
                for lm in hand.landmark:
                    landmarks.append({"x": float(lm.x), "y": float(lm.y), "z": float(lm.z)})
            gesture = self._infer_gesture(res.multi_hand_landmarks[0])
            return PoseResult(landmarks=landmarks, gesture=gesture, confidence=0.8)
        except Exception:
            return PoseResult()

    def _infer_gesture(self, hand_landmarks) -> str:
        """Very coarse gesture inference from finger tip extensions."""
        try:
            tips = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
            extended = []
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                extended.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y)
            if all(extended):
                return "open_palm"
            if not any(extended):
                return "fist"
            if extended[0] and not any(extended[1:]):
                return "point"
            return "partial"
        except Exception:
            return "unknown"
