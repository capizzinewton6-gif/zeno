"""Facial landmark alignment (5-point / 68-point) for embedding extraction."""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from calculations.landmark_transforms import align_points, ARCFACE_TEMPLATE


class FaceAligner:
    """Detect landmarks and warp faces to a canonical pose via similarity transform."""

    def __init__(self, output_size: int = 112) -> None:
        self.output_size = output_size
        self._mp_face_mesh = None

    def detect_landmarks(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """Return up to 5 landmarks for the face, or None if unavailable."""
        try:
            import mediapipe as mp  # type: ignore
            if self._mp_face_mesh is None:
                self._mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
                    static_image_mode=True, max_num_faces=1,
                    refine_landmarks=True, min_detection_confidence=0.5)
            rgb = face_image[:, :, ::-1] if face_image.ndim == 3 else face_image
            res = self._mp_face_mesh.process(rgb)
            if not res.multi_face_landmarks:
                return None
            lms = res.multi_face_landmarks[0].landmark
            h, w = face_image.shape[:2]
            # MediaPipe face mesh key indices approximating the ArcFace 5-point set
            idx = [33, 263, 1, 61, 291]  # left eye, right eye, nose, mouth left, mouth right
            pts = np.array([[lms[i].x * w, lms[i].y * h] for i in idx], dtype=np.float32)
            return pts
        except Exception:
            return None

    def align(self, face_image: np.ndarray,
              landmarks: Optional[np.ndarray] = None) -> np.ndarray:
        if landmarks is None:
            landmarks = self.detect_landmarks(face_image)
        if landmarks is None or len(landmarks) < 5:
            # Fallback: simple centered resize
            try:
                import cv2  # type: ignore
                return cv2.resize(face_image, (self.output_size, self.output_size))
            except Exception:
                return face_image
        try:
            import cv2  # type: ignore
            m = align_points(landmarks, ARCFACE_TEMPLATE, self.output_size)
            return cv2.warpAffine(face_image, m, (self.output_size, self.output_size),
                                  borderValue=0)
        except Exception:
            return face_image
