"""Spatial feature extraction: keypoints and descriptors (ORB/SIFT via OpenCV)."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


class FeatureExtractor:
    """Keypoint + descriptor extractor for image matching / re-id."""

    def __init__(self, method: str = "orb", max_features: int = 500) -> None:
        self.method = method
        self.max_features = max_features
        self._extractor = None

    def _ensure(self) -> None:
        if self._extractor is not None:
            return
        try:
            import cv2  # type: ignore
            if self.method == "sift":
                self._extractor = cv2.SIFT_create(self.max_features)
            else:
                self._extractor = cv2.ORB_create(self.max_features)
        except Exception:
            self._extractor = None

    def extract(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        self._ensure()
        if self._extractor is None:
            return [], np.zeros((0, 32), dtype=np.uint8)
        gray = image if image.ndim == 2 else image[:, :, 0]
        kps, des = self._extractor.detectAndCompute(gray, None)
        return list(kps), des if des is not None else np.zeros((0, 32), dtype=np.uint8)

    @staticmethod
    def match(des_a: np.ndarray, des_b: np.ndarray, ratio: float = 0.75) -> int:
        """Return number of good matches (Lowe ratio test)."""
        if des_a is None or des_b is None or len(des_a) < 2 or len(des_b) < 2:
            return 0
        try:
            import cv2  # type: ignore
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            raw = bf.knnMatch(des_a, des_b, k=2)
            good = [m for m, n in raw if m.distance < ratio * n.distance]
            return len(good)
        except Exception:
            return 0
