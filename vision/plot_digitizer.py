"""Extract data points from experimental phase diagrams and spectra."""

from __future__ import annotations

import numpy as np


class PlotDigitizer:
    """Recover data points from rendered curves (polynomial-fit / centroid sampling)."""

    @staticmethod
    def linearize_curve(x_pixels: np.ndarray, y_pixels: np.ndarray,
                        x_range: tuple[float, float], y_range: tuple[float, float]) -> np.ndarray:
        """Map pixel coordinates to data coordinates given axis ranges."""
        x0, x1 = x_range
        y0, y1 = y_range
        xp = np.asarray(x_pixels, dtype=float)
        yp = np.asarray(y_pixels, dtype=float)
        # assume pixels span the axis range linearly
        xs = x0 + (xp - xp.min()) / max(xp.ptp(), 1e-9) * (x1 - x0)
        ys = y1 - (yp - yp.min()) / max(yp.ptp(), 1e-9) * (y1 - y0)  # y axis inverted in plots
        return np.vstack([xs, ys]).T

    @staticmethod
    def peak_find(spectrum: np.ndarray, prominence: float = 0.1) -> np.ndarray:
        """Simple local-maximum peak finder."""
        s = np.asarray(spectrum, dtype=float)
        peaks = []
        for i in range(1, len(s) - 1):
            if s[i] > s[i - 1] and s[i] > s[i + 1] and s[i] > prominence * s.max():
                peaks.append(i)
        return np.array(peaks)
