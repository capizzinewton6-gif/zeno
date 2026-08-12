"""Engineering data analyzer."""

from __future__ import annotations

from typing import List

import numpy as np


class DataAnalyzer:
    def statistics(self, data: List[float]) -> dict:
        arr = np.array(data, dtype=float)
        return {"mean": float(arr.mean()), "median": float(np.median(arr)),
                "std": float(arr.std()), "var": float(arr.var()),
                "min": float(arr.min()), "max": float(arr.max()),
                "count": int(arr.size)}

    def linear_regression(self, x: List[float], y: List[float]) -> dict:
        xa, ya = np.array(x, dtype=float), np.array(y, dtype=float)
        n = len(xa)
        slope = (n * np.sum(xa * ya) - np.sum(xa) * np.sum(ya)) / \
                (n * np.sum(xa ** 2) - np.sum(xa) ** 2)
        intercept = (np.sum(ya) - slope * np.sum(xa)) / n
        r = np.corrcoef(xa, ya)[0, 1]
        return {"slope": float(slope), "intercept": float(intercept),
                "r": float(r), "r_squared": float(r ** 2)}

    def moving_average(self, data: List[float], window: int = 3) -> List[float]:
        arr = np.array(data, dtype=float)
        if window <= 1:
            return arr.tolist()
        return np.convolve(arr, np.ones(window) / window, mode="valid").tolist()

    def fft(self, data: List[float]) -> dict:
        arr = np.array(data, dtype=float)
        spectrum = np.fft.rfft(arr)
        freqs = np.fft.rfftfreq(len(arr))
        return {"frequencies": freqs.tolist(),
                "amplitudes": np.abs(spectrum).tolist()}

    def outlier_zscore(self, data: List[float], threshold: float = 2.0) -> List[int]:
        arr = np.array(data, dtype=float)
        z = (arr - arr.mean()) / arr.std() if arr.std() else np.zeros_like(arr)
        return [int(i) for i in np.where(np.abs(z) > threshold)[0]]
