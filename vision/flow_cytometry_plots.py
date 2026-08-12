"""Gating visualization from image exports."""
from __future__ import annotations

import numpy as np


class FlowCytometryPlots:
    @staticmethod
    def quadrant_gating(fluor1: list[float], fluor2: list[float],
                         threshold1: float, threshold2: float) -> dict:
        """Quadrant gating counts."""
        f1, f2 = np.array(fluor1), np.array(fluor2)
        q1 = int(np.sum((f1 > threshold1) & (f2 > threshold2)))   # double positive
        q2 = int(np.sum((f1 <= threshold1) & (f2 > threshold2)))  # F2+
        q3 = int(np.sum((f1 <= threshold1) & (f2 <= threshold2)))  # double negative
        q4 = int(np.sum((f1 > threshold1) & (f2 <= threshold2)))  # F1+
        return {"Q1_double_pos": q1, "Q2_F2_pos": q2,
                "Q3_double_neg": q3, "Q4_F1_pos": q4,
                "thresholds": [threshold1, threshold2]}

    @staticmethod
    def percentage_gated(events: list[float], threshold: float) -> float:
        arr = np.array(events)
        if len(arr) == 0:
            return 0.0
        return round(100.0 * float(np.sum(arr > threshold) / len(arr)), 2)

    @staticmethod
    def histogram(events: list[float], n_bins: int = 50) -> dict:
        arr = np.array(events)
        counts, edges = np.histogram(arr, bins=n_bins)
        return {"counts": counts.tolist(), "bin_edges": edges.tolist()}
