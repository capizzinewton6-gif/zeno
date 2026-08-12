"""Analyze colors on screen."""

from __future__ import annotations

import logging
from collections import Counter
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class ColorAnalyzer:
    """Analyzes the color composition of a screen image."""

    def dominant_colors(self, image: Any, n: int = 5) -> List[Tuple[Tuple[int, int, int], int]]:
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is None:
                return []
            pixels = arr.reshape(-1, arr.shape[-1])[:, :3]
            quantized = (pixels // 32 * 32)
            counts = Counter(map(tuple, quantized.tolist()))
            return counts.most_common(n)
        except Exception as exc:
            logger.debug("dominant_colors failed: %s", exc)
            return []

    def color_distribution(self, image: Any) -> Dict[str, float]:
        """Return the fraction of warm, cool, and neutral pixels."""
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is None:
                return {"warm": 0, "cool": 0, "neutral": 0}
            pixels = arr.reshape(-1, arr.shape[-1])[:, :3].astype(int)
            r, g, b = pixels[:, 0], pixels[:, 1], pixels[:, 2]
            warm = ((r > b) & (r > 80)).mean()
            cool = ((b > r) & (b > 80)).mean()
            neutral = 1.0 - warm - cool
            return {"warm": round(float(warm), 3), "cool": round(float(cool), 3),
                    "neutral": round(float(neutral), 3)}
        except Exception as exc:
            logger.debug("color_distribution failed: %s", exc)
            return {"warm": 0, "cool": 0, "neutral": 0}

    def average_color(self, image: Any) -> Tuple[int, int, int]:
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is None:
                return (0, 0, 0)
            return tuple(int(x) for x in arr[:, :, :3].mean(axis=(0, 1)))
        except Exception:
            return (0, 0, 0)

    def is_grayscale(self, image: Any) -> bool:
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is None or arr.ndim < 3:
                return True
            r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
            return bool(np.allclose(r, g, atol=5) and np.allclose(g, b, atol=5))
        except Exception:
            return False
