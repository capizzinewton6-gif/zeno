"""Track movement on screen."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class MotionAnalyzer:
    """Detects motion vectors between consecutive frames."""

    def __init__(self, block_size: int = 16, search_radius: int = 8) -> None:
        self.block_size = block_size
        self.search_radius = search_radius

    def optical_flow(self, image_before: Any, image_after: Any) -> List[Dict[str, Any]]:
        try:
            import cv2  # type: ignore
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            a = ImageAnalyzer._to_array(image_before)
            b = ImageAnalyzer._to_array(image_after)
            if a is None or b is None:
                return []
            gray_a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
            gray_b = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
            flow = cv2.calcOpticalFlowFarneback(gray_a, gray_b, None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)
            h, w = gray_a.shape
            results = []
            step = self.block_size
            for y in range(0, h, step):
                for x in range(0, w, step):
                    fx, fy = flow[y, x]
                    if abs(fx) > 0.5 or abs(fy) > 0.5:
                        results.append({
                            "position": [int(x), int(y)],
                            "displacement": [round(float(fx), 2), round(float(fy), 2)],
                            "magnitude": round(float((fx**2 + fy**2) ** 0.5), 2),
                        })
            return results
        except Exception as exc:
            logger.debug("optical_flow failed: %s", exc)
            return []

    def motion_intensity(self, image_before: Any, image_after: Any) -> float:
        vectors = self.optical_flow(image_before, image_after)
        if not vectors:
            return 0.0
        return sum(v["magnitude"] for v in vectors) / len(vectors)

    def motion_region(self, image_before: Any, image_after: Any) -> Tuple[int, int, int, int] | None:
        try:
            from computer_vision.change_detector import ChangeDetector
            return ChangeDetector().change_region(image_before, image_after)
        except Exception:
            return None
