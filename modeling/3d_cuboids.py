"""3D bounding cuboids: construction, projection, and rendering geometry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

import numpy as np


@dataclass
class Cuboid3D:
    """A 3D bounding box defined by a center, dimensions, and yaw (radians)."""

    cx: float
    cy: float
    cz: float
    w: float
    l: float  # noqa: E741  (length, conventional in 3D detection)
    h: float
    yaw: float = 0.0
    label: str = ""
    confidence: float = 0.0

    @property
    def corners(self) -> np.ndarray:
        """Return the 8 corner points (8 x 3) in world coordinates."""
        x, y, z = self.cx, self.cy, self.cz
        dx, dy, dz = self.l / 2.0, self.w / 2.0, self.h / 2.0
        # 8 corners in local coordinates
        local = np.array([
            [dx, dy, dz], [dx, dy, -dz], [dx, -dy, dz], [dx, -dy, -dz],
            [-dx, dy, dz], [-dx, dy, -dz], [-dx, -dy, dz], [-dx, -dy, -dz],
        ], dtype=np.float32)
        c, s = np.cos(self.yaw), np.sin(self.yaw)
        rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float32)
        return local @ rot.T + np.array([x, y, z], dtype=np.float32)

    def project(self, intrinsic: np.ndarray) -> np.ndarray:
        """Project 8 corners to the image plane using a 3x3 intrinsic matrix.

        Returns an (8 x 2) array of pixel coordinates.
        """
        pts = self.corners
        proj = (intrinsic @ pts.T).T  # (8 x 3)
        proj = proj[:, :2] / np.clip(proj[:, 2:3], 1e-6, None)
        return proj[:, :2]


def cuboid_from_2d(bbox_xyxy: Sequence[float], depth_m: float, intrinsic: np.ndarray,
                   label: str = "", confidence: float = 0.0, height_m: float = 1.7) -> Cuboid3D:
    """Approximate a 3D cuboid from a 2D box + estimated depth using camera intrinsics."""
    x1, y1, x2, y2 = bbox_xyxy
    fx = intrinsic[0, 0]
    fy = intrinsic[1, 1]
    cx, cy = intrinsic[0, 2], intrinsic[1, 2]
    # back-project box center
    uv = np.array([(x1 + x2) / 2, (y1 + y2) / 2, 1.0])
    ray = np.linalg.inv(intrinsic) @ uv
    ray = ray / ray[2]
    center = ray * depth_m
    w_m = (x2 - x1) * depth_m / fx
    l_m = (x2 - x1) * depth_m / fx  # use width as length proxy
    h_m = (y2 - y1) * depth_m / fy
    return Cuboid3D(center[0], center[1], center[2] - h_m / 2.0,
                    w_m, l_m, h_m if h_m > 0 else height_m, yaw=0.0,
                    label=label, confidence=confidence)
