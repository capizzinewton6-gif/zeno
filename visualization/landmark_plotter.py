"""Landmark plotter: draws facial mesh grids, keypoints, direction vectors."""

from __future__ import annotations

from typing import List, Optional

import numpy as np


class LandmarkPlotter:
    """Draw keypoints, mesh connections, and head-pose direction vectors."""

    def __init__(self, radius: int = 2, color=(0, 255, 0)) -> None:
        self.radius = radius
        self.color = color

    def plot_points(self, image: np.ndarray, points: np.ndarray,
                    color=None) -> np.ndarray:
        out = image.copy()
        color = color or self.color
        try:
            import cv2  # type: ignore
            for p in np.asarray(points).reshape(-1, 2):
                x, y = int(p[0]), int(p[1])
                cv2.circle(out, (x, y), self.radius, color, -1)
        except Exception:
            pass
        return out

    def plot_mesh(self, image: np.ndarray, points: np.ndarray,
                  connections: Optional[List[tuple]] = None) -> np.ndarray:
        out = image.copy()
        try:
            import cv2  # type: ignore
            pts = np.asarray(points).reshape(-1, 2)
            if connections is None:
                connections = [(i, i + 1) for i in range(len(pts) - 1)]
            for a, b in connections:
                if a < len(pts) and b < len(pts):
                    cv2.line(out, (int(pts[a, 0]), int(pts[a, 1])),
                             (int(pts[b, 0]), int(pts[b, 1])), self.color, 1)
        except Exception:
            pass
        return out

    def plot_pose_vector(self, image: np.ndarray, origin, vector,
                         length: int = 50, color=(0, 0, 255)) -> np.ndarray:
        out = image.copy()
        try:
            import cv2  # type: ignore
            ox, oy = int(origin[0]), int(origin[1])
            vx, vy = vector
            norm = max(float((vx ** 2 + vy ** 2) ** 0.5), 1e-6)
            ex = int(ox + vx / norm * length)
            ey = int(oy + vy / norm * length)
            cv2.arrowedLine(out, (ox, oy), (ex, ey), color, 2)
        except Exception:
            pass
        return out
