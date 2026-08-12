"""Cell counting, fluorescence, and morphology analysis."""
from __future__ import annotations

import numpy as np


class MicroscopyAnalyzer:
    @staticmethod
    def count_cells(binary_image: np.ndarray) -> dict:
        """Count connected components in a binary mask."""
        from scipy import ndimage
        if binary_image.dtype != bool:
            binary_image = binary_image > 0
        labeled, n = ndimage.label(binary_image)
        if n == 0:
            return {"count": 0, "mean_area_px": 0}
        sizes = ndimage.sum(binary_image, labeled, range(1, n + 1))
        return {"count": int(n), "mean_area_px": round(float(np.mean(sizes)), 2),
                "total_area_px": int(np.sum(binary_image))}

    @staticmethod
    def mean_fluorescence(image: np.ndarray, mask: np.ndarray | None = None) -> float:
        if image.ndim == 3:
            image = image.mean(axis=2)
        if mask is not None:
            vals = image[mask > 0]
        else:
            vals = image.flatten()
        return round(float(vals.mean()), 4)

    @staticmethod
    def morphology_metrics(binary_image: np.ndarray) -> dict:
        from scipy import ndimage
        labeled, n = ndimage.label(binary_image > 0)
        if n == 0:
            return {"n_objects": 0}
        areas = ndimage.sum(binary_image, labeled, range(1, n + 1))
        # rough aspect ratio from bounding boxes
        ratios = []
        for i in range(1, n + 1):
            ys, xs = np.where(labeled == i)
            if len(xs) > 1 and len(ys) > 1:
                w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
                ratios.append(max(w, h) / max(min(w, h), 1))
        return {
            "n_objects": int(n),
            "mean_area_px": round(float(np.mean(areas)), 2),
            "mean_aspect_ratio": round(float(np.mean(ratios)) if ratios else 0, 3),
        }

    @staticmethod
    def confluence(binary_image: np.ndarray) -> float:
        return round(100.0 * float(np.sum(binary_image > 0)) / binary_image.size, 2)
