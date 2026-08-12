"""Apparatus analyzer: camera angle, lens cleanliness, occlusion warnings."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ApparatusReport:
    angle_ok: bool
    lens_clean: bool
    occluded: bool
    notes: list


class ApparatusAnalyzer:
    """Warn about camera-hardware issues (dirty lens, tilt, occlusion)."""

    def __init__(self, edge_ratio: float = 0.3, dirt_std: float = 5.0,
                 occlusion_area: float = 0.4) -> None:
        self.edge_ratio = edge_ratio
        self.dirt_std = dirt_std
        self.occlusion_area = occlusion_area

    def analyze(self, image: np.ndarray) -> ApparatusReport:
        notes = []
        if image is None or image.size == 0:
            return ApparatusReport(False, False, True, ["empty_frame"])
        gray = image.mean(axis=2) if image.ndim == 3 else image

        edge_ratio = self._edge_ratio(gray)
        angle_ok = edge_ratio < (1.0 - self.edge_ratio)
        if not angle_ok:
            notes.append(f"possible_tilt(edge_ratio={edge_ratio:.2f})")

        std = float(gray.std())
        lens_clean = std >= self.dirt_std
        if not lens_clean:
            notes.append(f"lens_maybe_dirty(std={std:.1f})")

        dark_ratio = float(np.mean(gray < 10))
        occluded = dark_ratio >= self.occlusion_area
        if occluded:
            notes.append(f"possible_occlusion(dark={dark_ratio:.2f})")

        return ApparatusReport(angle_ok=angle_ok, lens_clean=lens_clean,
                               occluded=occluded, notes=notes)

    @staticmethod
    def _edge_ratio(gray: np.ndarray) -> float:
        try:
            import cv2  # type: ignore
            edges = cv2.Canny(gray.astype(np.uint8), 50, 150)
            border = np.zeros_like(edges)
            h, w = edges.shape
            border[:max(1, h // 10), :] = 1
            border[-max(1, h // 10):, :] = 1
            border[:, :max(1, w // 10)] = 1
            border[:, -max(1, w // 10):] = 1
            border_edges = float(np.sum(edges * border > 0))
            total_edges = max(float(np.sum(edges > 0)), 1.0)
            return border_edges / total_edges
        except Exception:
            return 0.0
