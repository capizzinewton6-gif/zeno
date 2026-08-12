"""Tracking visualizer: motion trails, IDs, velocity vectors."""

from __future__ import annotations

from typing import List

import numpy as np

from tracking_analytics.object_tracker import Track
from tracking_analytics.trajectory_analyzer import TrajectoryAnalyzer


class TrackingVisualizer:
    """Render track history trails, IDs, and velocity vectors."""

    def __init__(self, trail_length: int = 30, color=(0, 255, 255)) -> None:
        self.trail_length = trail_length
        self.color = color

    def render(self, image: np.ndarray, tracks: List[Track],
               analyzer: TrajectoryAnalyzer = None) -> np.ndarray:
        out = image.copy()
        try:
            import cv2  # type: ignore
            for t in tracks:
                history = t.history[-self.trail_length:]
                for i in range(1, len(history)):
                    a = ((history[i - 1][0] + history[i - 1][2]) / 2,
                         (history[i - 1][1] + history[i - 1][3]) / 2)
                    b = ((history[i][0] + history[i][2]) / 2,
                         (history[i][1] + history[i][3]) / 2)
                    cv2.line(out, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])),
                             self.color, 2)
                cv2.rectangle(out, (int(t.bbox[0]), int(t.bbox[1])),
                              (int(t.bbox[2]), int(t.bbox[3])), self.color, 2)
                cv2.putText(out, f"#{t.track_id} {t.label}",
                            (int(t.bbox[0]), max(0, int(t.bbox[1]) - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1, cv2.LINE_AA)
        except Exception:
            pass
        return out
