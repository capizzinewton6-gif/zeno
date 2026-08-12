"""Detect patterns in screen images."""

from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PatternRecognition:
    """Detects repeating visual patterns on screen."""

    def hash_image(self, image: Any) -> str:
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is not None:
                small = arr[::16, ::16]
                return hashlib.md5(small.tobytes()).hexdigest()
        except Exception as exc:
            logger.debug("hash_image failed: %s", exc)
        return hashlib.md5(str(id(image)).encode()).hexdigest()

    def grid_pattern(self, image: Any, cell_size: int = 32) -> List[List[float]]:
        """Return a coarse grid of mean brightness values for pattern inspection."""
        try:
            import numpy as np  # type: ignore
            from computer_vision.image_analyzer import ImageAnalyzer
            arr = ImageAnalyzer._to_array(image)
            if arr is None:
                return []
            gray = arr.mean(axis=-1) if arr.ndim == 3 else arr
            h, w = gray.shape
            rows = h // cell_size
            cols = w // cell_size
            grid = []
            for r in range(rows):
                row = []
                for c in range(cols):
                    block = gray[r*cell_size:(r+1)*cell_size, c*cell_size:(c+1)*cell_size]
                    row.append(round(float(block.mean()), 1))
                grid.append(row)
            return grid
        except Exception as exc:
            logger.debug("grid_pattern failed: %s", exc)
            return []

    def is_repeating(self, image: Any, min_repeats: int = 2) -> bool:
        grid = self.grid_pattern(image)
        if not grid:
            return False
        flat = [v for row in grid for v in row]
        counts: Dict[float, int] = {}
        for v in flat:
            counts[v] = counts.get(v, 0) + 1
        return any(c >= min_repeats for c in counts.values())

    def similarity(self, image_a: Any, image_b: Any) -> float:
        ha = self.hash_image(image_a)
        hb = self.hash_image(image_b)
        if ha == hb:
            return 1.0
        # Hamming distance over hex chars
        return 1.0 - sum(a != b for a, b in zip(ha, hb)) / max(len(ha), len(hb))
