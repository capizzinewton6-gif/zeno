"""Unit converter: pixel space, normalized coordinates, meters."""

from __future__ import annotations

from typing import Sequence, Tuple


def px_to_normalized(box_xyxy: Sequence[float], width: int, height: int) -> list:
    x1, y1, x2, y2 = box_xyxy
    return [x1 / width, y1 / height, x2 / width, y2 / height]


def normalized_to_px(box_norm: Sequence[float], width: int, height: int) -> list:
    x1, y1, x2, y2 = box_norm
    return [x1 * width, y1 * height, x2 * width, y2 * height]


def px_to_meters(pixel_value: float, depth_m: float, focal_px: float) -> float:
    return float(pixel_value * depth_m / max(focal_px, 1e-6))


def meters_to_px(meters: float, depth_m: float, focal_px: float) -> float:
    return float(meters * max(focal_px, 1e-6) / max(depth_m, 1e-6))


def deg_to_rad(deg: float) -> float:
    return deg * 3.141592653589793 / 180.0


def rad_to_deg(rad: float) -> float:
    return rad * 180.0 / 3.141592653589793
