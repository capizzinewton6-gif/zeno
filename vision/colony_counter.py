"""Automated CFU counting on agar plates."""
from __future__ import annotations

import numpy as np


class ColonyCounter:
    @staticmethod
    def count(image: np.ndarray, min_area: int = 5, max_area: int = 2000,
               dilution_factor: int = 1, plate_area_cm2: float = 56.7) -> dict:
        """Count distinct colonies from a binary/thresholded image."""
        from scipy import ndimage
        if image.ndim == 3:
            image = image.mean(axis=2)
        # threshold: assume colonies are darker or a pre-binarized mask
        binary = image > image.mean()
        labeled, n = ndimage.label(binary)
        sizes = ndimage.sum(binary, labeled, range(1, n + 1)) if n else []
        valid = [s for s in sizes if min_area <= s <= max_area]
        count = len(valid)
        cfu_per_cm2 = count / max(plate_area_cm2, 1e-9)
        return {
            "colonies_counted": count,
            "excluded_too_small": sum(1 for s in sizes if s < min_area),
            "excluded_too_large": sum(1 for s in sizes if s > max_area),
            "dilution_factor": dilution_factor,
            "cfu_per_cm2": round(cfu_per_cm2, 2),
            "cfu_per_plate": count * dilution_factor,
        }

    @staticmethod
    def colony_size_distribution(image: np.ndarray) -> list[float]:
        from scipy import ndimage
        if image.ndim == 3:
            image = image.mean(axis=2)
        binary = image > image.mean()
        labeled, n = ndimage.label(binary)
        if n == 0:
            return []
        sizes = ndimage.sum(binary, labeled, range(1, n + 1))
        return [round(float(s), 2) for s in sizes]
