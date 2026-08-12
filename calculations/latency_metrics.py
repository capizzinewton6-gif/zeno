"""Latency metrics: FPS, latency breakdowns, throughput statistics."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict


@dataclass
class LatencyMetrics:
    window: int = 100
    _stamps: Deque[float] = field(default_factory=lambda: deque(maxlen=100))
    _stage_times: Dict[str, Deque[float]] = field(default_factory=dict)

    def tick(self) -> None:
        self._stamps.append(time.perf_counter())

    def record_stage(self, name: str, seconds: float) -> None:
        if name not in self._stage_times:
            self._stage_times[name] = deque(maxlen=self.window)
        self._stage_times[name].append(seconds)

    @property
    def fps(self) -> float:
        if len(self._stamps) < 2:
            return 0.0
        elapsed = self._stamps[-1] - self._stamps[0]
        if elapsed <= 0:
            return 0.0
        return (len(self._stamps) - 1) / elapsed

    def stage_stats(self, name: str) -> Dict[str, float]:
        times = list(self._stage_times.get(name, []))
        if not times:
            return {"count": 0, "mean_ms": 0.0, "max_ms": 0.0}
        arr = [t * 1000.0 for t in times]
        return {"count": len(arr), "mean_ms": sum(arr) / len(arr), "max_ms": max(arr)}

    def summary(self) -> Dict[str, float]:
        out = {"fps": self.fps}
        for name in self._stage_times:
            stats = self.stage_stats(name)
            out[f"{name}_mean_ms"] = stats["mean_ms"]
            out[f"{name}_max_ms"] = stats["max_ms"]
        return out
