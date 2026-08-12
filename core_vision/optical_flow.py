"""Optical flow: Lucas-Kanade (sparse) and Farneback (dense)."""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np


class OpticalFlow:
    """Compute sparse (Lucas-Kanade) and dense (Farneback) optical flow."""

    def __init__(self) -> None:
        self._prev_gray = None
        self._lk_params = dict(winSize=(15, 15), maxLevel=2,
                               criteria=(3, 10, 0.03))  # (TERM_CRITERIA_EPS|COUNT, ...)
        self._points = None

    @staticmethod
    def _to_gray(image: np.ndarray) -> np.ndarray:
        if image.ndim == 2:
            return image
        try:
            import cv2  # type: ignore
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return image[:, :, 0]

    def lucas_kanade(self, image: np.ndarray, points: np.ndarray) -> np.ndarray:
        """Track sparse points from previous frame to current. Returns new points."""
        try:
            import cv2  # type: ignore
        except Exception:  # pragma: no cover
            return points
        gray = self._to_gray(image)
        if self._prev_gray is None or points is None or len(points) == 0:
            self._prev_gray = gray
            self._points = points.reshape(-1, 1, 2).astype(np.float32) if points is not None else None
            return points
        pts = points.reshape(-1, 1, 2).astype(np.float32)
        new_pts, status, _ = cv2.calcOpticalFlowPyrLK(self._prev_gray, gray, pts, None, **self._lk_params)
        self._prev_gray = gray
        if new_pts is None:
            return points
        good = new_pts[status.ravel() == 1]
        return good.reshape(-1, 2) if len(good) else points

    def farneback(self, prev: np.ndarray, curr: np.ndarray) -> Optional[np.ndarray]:
        """Dense optical flow (HxWx2). Returns None if OpenCV unavailable."""
        try:
            import cv2  # type: ignore
        except Exception:  # pragma: no cover
            return None
        g0 = self._to_gray(prev)
        g1 = self._to_gray(curr)
        return cv2.calcOpticalFlowFarneback(g0, g1, None, 0.5, 3, 15, 3, 5, 1.1, 0)
