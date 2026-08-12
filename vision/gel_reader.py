"""Agarose/SDS-PAGE gel band analyzer."""
from __future__ import annotations

import numpy as np


class GelReader:
    @staticmethod
    def detect_lanes(image_array: np.ndarray, n_expected: int = 0) -> list[dict]:
        """Detect vertical lanes by column-intensity variance (1D lanes).

        image_array: 2D grayscale array, lanes vertical.
        """
        if image_array.ndim == 3:
            gray = image_array.mean(axis=2)
        else:
            gray = image_array
        col_sums = gray.sum(axis=0)
        threshold = col_sums.mean()
        in_lane = col_sums < threshold
        lanes = []
        i = 0
        while i < len(in_lane):
            if in_lane[i]:
                start = i
                while i < len(in_lane) and in_lane[i]:
                    i += 1
                end = i
                if end - start > 3:
                    lanes.append({"lane_index": len(lanes) + 1,
                                  "start_x": start, "end_x": end,
                                  "width": end - start})
            else:
                i += 1
        if n_expected and len(lanes) > n_expected:
            # keep the n_expected brightest (lowest sum = darkest band region)
            lanes_sorted = sorted(lanes,
                                  key=lambda l: col_sums[l["start_x"]:l["end_x"]].mean())[:n_expected]
            lanes = sorted(lanes_sorted, key=lambda l: l["start_x"])
        return lanes

    @staticmethod
    def band_sizes(ladder_sizes: list[int], ladder_distances: list[float],
                   sample_distances: list[float]) -> list[int]:
        """Interpolate band sizes from a DNA ladder.

        Uses a log-linear relationship between size and migration distance.
        """
        log_sizes = np.log(ladder_sizes)
        coeffs = np.polyfit(ladder_distances, log_sizes, 1)
        return [int(round(np.exp(np.polyval(coeffs, d)))) for d in sample_distances]

    @staticmethod
    def estimate_concentration(band_intensity: float,
                                ladder_intensity: float,
                                ladder_mass_ng: float) -> float:
        if ladder_intensity <= 0:
            return 0.0
        return round(band_intensity / ladder_intensity * ladder_mass_ng, 2)
