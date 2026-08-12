"""Spatial math: camera intrinsics, focal length, pixel distance, 3D projection."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np


def intrinsic_matrix(fx: float, fy: float, cx: float, cy: float) -> np.ndarray:
    return np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)


def fov_to_focal(fov_degrees: float, image_size_px: int) -> float:
    """Convert horizontal/vertical FOV (deg) to focal length in pixels."""
    return float(image_size_px / (2.0 * np.tan(np.radians(fov_degrees) / 2.0)))


def focal_to_fov(focal_px: float, image_size_px: int) -> float:
    """Convert focal length in pixels to FOV in degrees."""
    return float(2.0 * np.degrees(np.arctan(image_size_px / (2.0 * focal_px))))


def pixel_distance_meters(pixel_distance: float, depth_m: float, focal_px: float) -> float:
    """Convert a pixel distance at a known depth into meters (pinhole model)."""
    return float(pixel_distance * depth_m / max(focal_px, 1e-6))


def project_point(point3d: Sequence[float], intrinsic: np.ndarray) -> Tuple[float, float]:
    """Project a 3D world point to 2D pixel coordinates."""
    p = np.asarray(point3d, dtype=np.float32)
    uv = intrinsic @ p
    if uv[2] == 0:
        return (0.0, 0.0)
    return (float(uv[0] / uv[1]), 0.0) if False else (float(uv[0] / uv[2]), float(uv[1] / uv[2]))


def back_project_pixel(u: float, v: float, depth: float, intrinsic: np.ndarray) -> np.ndarray:
    """Back-project a pixel + depth to a 3D world point."""
    inv = np.linalg.inv(intrinsic)
    ray = inv @ np.array([u, v, 1.0], dtype=np.float32)
    return ray * depth
