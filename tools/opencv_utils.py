"""Custom OpenCV wrappers for video capture and manipulation."""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np


class OpenCVUtils:
    """Convenience wrappers around common OpenCV operations."""

    @staticmethod
    def read_image(path: str) -> Optional[np.ndarray]:
        try:
            import cv2  # type: ignore
            return cv2.imread(path)
        except Exception:
            return None

    @staticmethod
    def write_image(path: str, image: np.ndarray) -> bool:
        try:
            import cv2  # type: ignore
            return bool(cv2.imwrite(path, image))
        except Exception:
            return False

    @staticmethod
    def resize(image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
        try:
            import cv2  # type: ignore
            return cv2.resize(image, size)
        except Exception:
            return image

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        if image.ndim == 2:
            return image
        try:
            import cv2  # type: ignore
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception:
            return image[:, :, 0]

    @staticmethod
    def rotate(image: np.ndarray, angle: float) -> np.ndarray:
        try:
            import cv2  # type: ignore
            h, w = image.shape[:2]
            m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
            return cv2.warpAffine(image, m, (w, h))
        except Exception:
            return image

    @staticmethod
    def stack_horizontal(images) -> np.ndarray:
        try:
            import cv2  # type: ignore
            return cv2.hconcat([np.asarray(im) for im in images])
        except Exception:
            return np.hstack([np.asarray(im) for im in images])
