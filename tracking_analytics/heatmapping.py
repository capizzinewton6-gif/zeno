"""Heatmapping: spatial occupancy and movement heatmaps."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from tracking_analytics.object_tracker import Track


class Heatmapper:
    """Accumulate detection/track centers into a 2D heatmap."""

    def __init__(self, height: int = 480, width: int = 640,
                 decay: float = 0.99, sigma: int = 15) -> None:
        self.height = height
        self.width = width
        self.decay = decay
        self.sigma = sigma
        self.grid = np.zeros((height, width), dtype=np.float32)

    def add_points(self, points: List[Tuple[float, float]], weight: float = 1.0) -> None:
        self.grid *= self.decay
        for x, y in points:
            xi, yi = int(x), int(y)
            if 0 <= xi < self.width and 0 <= yi < self.height:
                self._add_gaussian(xi, yi, weight)

    def add_tracks(self, tracks: List[Track]) -> None:
        pts = []
        for t in tracks:
            cx = (t.bbox[0] + t.bbox[2]) / 2.0
            cy = (t.bbox[1] + t.bbox[3]) / 2.0
            pts.append((cx, cy))
        self.add_points(pts)

    def _add_gaussian(self, cx: int, cy: int, weight: float) -> None:
        try:
            import cv2  # type: ignore
            size = max(1, self.sigma * 4)
            x0 = max(0, cx - size)
            x1 = min(self.width, cx + size)
            y0 = max(0, cy - size)
            y1 = min(self.height, cy + size)
            if x1 <= x0 or y1 <= y0:
                return
            gauss = np.zeros((y1 - y0, x1 - x0), dtype=np.float32)
            gauss[(y1 - y0) // 2, (x1 - x0) // 2] = weight
            gauss = cv2.GaussianBlur(gauss, (0, 0), self.sigma)
            self.grid[y0:y1, x0:x1] += gauss
        except Exception:
            if 0 <= cy < self.height and 0 <= cx < self.width:
                self.grid[cy, cx] += weight

    def render(self) -> np.ndarray:
        """Return a uint8 color heatmap (HxWx3)."""
        try:
            import cv2  # type: ignore
            norm = cv2.normalize(self.grid, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            return cv2.applyColorMap(norm, cv2.COLORMAP_JET)
        except Exception:
            norm = (np.clip(self.grid / (self.grid.max() + 1e-6), 0, 1) * 255).astype(np.uint8)
            return np.stack([norm, norm, norm], axis=-1)

    def reset(self) -> None:
        self.grid.fill(0.0)
