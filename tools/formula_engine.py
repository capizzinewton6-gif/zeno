"""Formula engine: resolution aspect ratios, FOV, sensor coverage."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SensorSpec:
    width_mm: float
    height_mm: float
    focal_mm: float


class FormulaEngine:
    """Compute common camera/imaging formulas."""

    @staticmethod
    def aspect_ratio(width: int, height: int) -> Tuple[int, int]:
        g = math.gcd(width, height)
        return (width // g, height // g)

    @staticmethod
    def diagonal(width: int, height: int) -> float:
        return math.hypot(width, height)

    @staticmethod
    def horizontal_fov(sensor: SensorSpec) -> float:
        return 2 * math.degrees(math.atan(sensor.width_mm / (2 * sensor.focal_mm)))

    @staticmethod
    def vertical_fov(sensor: SensorSpec) -> float:
        return 2 * math.degrees(math.atan(sensor.height_mm / (2 * sensor.focal_mm)))

    @staticmethod
    def ground_coverage(distance_m: float, fov_deg: float) -> float:
        return 2 * distance_m * math.tan(math.radians(fov_deg / 2))

    @staticmethod
    def pixel_density(object_width_m: float, distance_m: float,
                      sensor: SensorSpec, image_width_px: int) -> float:
        """Pixels-per-meter for an object at a given distance."""
        fov = FormulaEngine.horizontal_fov(sensor)
        coverage = FormulaEngine.ground_coverage(distance_m, fov)
        if coverage <= 0:
            return 0.0
        return (image_width_px / coverage) * object_width_m
