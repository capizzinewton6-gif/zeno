"""Detect screen changes between frames."""

from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


class ChangeDetector:
    """Detects pixel-level differences between two screen captures."""

    def __init__(self, threshold: float = 0.01) -> None:
        self.threshold = threshold

    def diff_ratio(self, image_before: Any, image_after: Any) -> float:
        """Return the fraction of pixels that changed (0.0 to 1.0)."""
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            a = ImageAnalyzer._to_array(image_before)
            b = ImageAnalyzer._to_array(image_after)
            if a is None or b is None:
                return 0.0
            if a.shape != b.shape:
                return 1.0
            gray_a = a.mean(axis=-1) if a.ndim == 3 else a
            gray_b = b.mean(axis=-1) if b.ndim == 3 else b
            diff = np.abs(gray_a.astype(int) - gray_b.astype(int)) > 15
            return float(diff.mean())
        except Exception as exc:
            logger.debug("diff_ratio failed: %s", exc)
            return 0.0

    def has_changed(self, image_before: Any, image_after: Any) -> bool:
        return self.diff_ratio(image_before, image_after) > self.threshold

    def change_region(self, image_before: Any, image_after: Any) -> Tuple[int, int, int, int] | None:
        """Return the bounding box (x, y, w, h) of changed pixels, or None."""
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            a = ImageAnalyzer._to_array(image_before)
            b = ImageAnalyzer._to_array(image_after)
            if a is None or b is None or a.shape != b.shape:
                return None
            gray_a = a.mean(axis=-1) if a.ndim == 3 else a
            gray_b = b.mean(axis=-1) if b.ndim == 3 else b
            diff = np.abs(gray_a.astype(int) - gray_b.astype(int)) > 15
            if not diff.any():
                return None
            rows = np.any(diff, axis=1)
            cols = np.any(diff, axis=0)
            y_min, y_max = np.where(rows)[0][[0, -1]]
            x_min, x_max = np.where(cols)[0][[0, -1]]
            return (int(x_min), int(y_min), int(x_max - x_min + 1), int(y_max - y_min + 1))
        except Exception as exc:
            logger.debug("change_region failed: %s", exc)
            return None

    def summarize(self, image_before: Any, image_after: Any) -> Dict[str, Any]:
        region = self.change_region(image_before, image_after)
        return {
            "ratio": self.diff_ratio(image_before, image_after),
            "changed": self.has_changed(image_before, image_after),
            "region": region,
        }
