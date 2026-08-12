"""Detect background noise anomalies, cosmic rays, and sensor glitches."""

from __future__ import annotations

import numpy as np
from scipy import stats


class AnomalyDetector:
    """Statistical anomaly detection in experimental data streams."""

    @staticmethod
    def z_score_outliers(data: np.ndarray, threshold: float = 5.0) -> np.ndarray:
        z = np.abs(stats.zscore(data, nan_policy="omit"))
        return np.where(z > threshold)[0]

    @staticmethod
    def cosmic_ray_spikes(spectrum: np.ndarray, window: int = 5, threshold: float = 6.0) -> np.ndarray:
        """Detect sharp single-bin spikes (cosmic-ray hits) via rolling median residual."""
        s = np.asarray(spectrum, dtype=float)
        med = np.median(np.lib.stride_tricks.sliding_window_view(s, window), axis=-1)
        pad = np.pad(med, (window // 2, window - 1 - window // 2), mode="edge")
        resid = np.abs(s - pad)
        mad = np.median(np.abs(pad - np.median(pad))) + 1e-9
        return np.where(resid / mad > threshold)[0]

    @staticmethod
    def sensor_glitches(data: np.ndarray, jump_threshold: float = 5.0) -> np.ndarray:
        """Detect sudden discontinuities (first-difference outliers)."""
        diffs = np.abs(np.diff(data))
        return np.where(diffs > jump_threshold * np.std(diffs) + 1e-9)[0]
