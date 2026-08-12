"""Real-time optical density and fluorescence data acquisition."""
from __future__ import annotations

import time
import random


class DataAcquisition:
    def __init__(self, channels: list[str] | None = None):
        self.channels = channels or ["OD600", "GFP", "mCherry"]
        self.buffer: list[dict] = []

    def sample(self, interval_s: float = 1.0, duration_s: float = 60,
               seed: int = 0) -> list[dict]:
        rng = random.Random(seed)
        t0 = time.time()
        readings = []
        n = max(int(duration_s / interval_s), 1)
        for i in range(n):
            row = {"time_s": round(i * interval_s, 2)}
            for ch in self.channels:
                row[ch] = round(rng.uniform(0.01, 1.0) * (1 + i * 0.01), 4)
            readings.append(row)
        self.buffer.extend(readings)
        return readings

    @staticmethod
    def growth_rate_from_od(od_series: list[float], interval_s: float = 1.0) -> float:
        import math
        if len(od_series) < 2:
            return 0.0
        n0, nt = od_series[0], od_series[-1]
        if n0 <= 0 or nt <= 0:
            return 0.0
        return math.log(nt / n0) / (len(od_series) * interval_s)

    def export(self) -> list[dict]:
        return self.buffer
