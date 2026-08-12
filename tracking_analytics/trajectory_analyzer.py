"""Trajectory analyzer: motion path logging, speed, boundary crossing."""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

from tracking_analytics.object_tracker import Track


class TrajectoryAnalyzer:
    """Derive motion statistics from a track's bounding-box history."""

    def __init__(self, fps: float = 30.0, pixels_per_meter: float = 50.0) -> None:
        self.fps = fps
        self.pixels_per_meter = pixels_per_meter

    def centers(self, track: Track) -> np.ndarray:
        if not track.history:
            return np.zeros((0, 2), dtype=np.float32)
        arr = np.array(track.history, dtype=np.float32)
        return np.stack([(arr[:, 0] + arr[:, 2]) / 2, (arr[:, 1] + arr[:, 3]) / 2], axis=1)

    def path_length_px(self, track: Track) -> float:
        centers = self.centers(track)
        if len(centers) < 2:
            return 0.0
        diffs = np.diff(centers, axis=0)
        return float(np.sum(np.sqrt(np.sum(diffs ** 2, axis=1))))

    def speed_mps(self, track: Track) -> float:
        if len(track.history) < 2:
            return 0.0
        length_m = self.path_length_px(track) / max(self.pixels_per_meter, 1e-6)
        duration_s = (len(track.history) - 1) / max(self.fps, 1e-6)
        return length_m / duration_s if duration_s > 0 else 0.0

    def crossed_boundary(self, track: Track, line: Tuple[float, float, float, float]) -> Optional[str]:
        """Detect if a track crossed a line segment (x1,y1)-(x2,y2). Returns direction."""
        centers = self.centers(track)
        if len(centers) < 2:
            return None
        x1, y1, x2, y2 = line
        def side(p):
            return (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
        prev_sign = np.sign(side(centers[0]))
        for c in centers[1:]:
            s = np.sign(side(c))
            if s != 0 and prev_sign != 0 and s != prev_sign:
                return "left_to_right" if s > 0 else "right_to_left"
            if s != 0:
                prev_sign = s
        return None
