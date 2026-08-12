"""Latency profiler: GPU memory, pipeline bottlenecks, frame drops."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict


@dataclass
class StageProfile:
    name: str
    calls: int = 0
    total_ms: float = 0.0
    max_ms: float = 0.0

    @property
    def avg_ms(self) -> float:
        return self.total_ms / max(self.calls, 1)


class LatencyProfiler:
    """Per-stage wall-clock profiler with rolling frame-drop counter."""

    def __init__(self, window: int = 100) -> None:
        self.stages: Dict[str, StageProfile] = {}
        self._frame_times: Deque[float] = deque(maxlen=window)
        self._stage_start: Dict[str, float] = {}
        self.dropped_frames = 0

    def start(self, stage: str) -> None:
        self._stage_start[stage] = time.perf_counter()

    def end(self, stage: str) -> float:
        start = self._stage_start.pop(stage, None)
        if start is None:
            return 0.0
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        s = self.stages.setdefault(stage, StageProfile(stage))
        s.calls += 1
        s.total_ms += elapsed_ms
        s.max_ms = max(s.max_ms, elapsed_ms)
        return elapsed_ms

    def frame_done(self) -> None:
        self._frame_times.append(time.perf_counter())

    def drop_frame(self) -> None:
        self.dropped_frames += 1

    def fps(self) -> float:
        if len(self._frame_times) < 2:
            return 0.0
        elapsed = self._frame_times[-1] - self._frame_times[0]
        return (len(self._frame_times) - 1) / max(elapsed, 1e-6)

    def summary(self) -> str:
        lines = [f"{'Stage':<24}{'calls':>8}{'avg(ms)':>10}{'max(ms)':>10}"]
        for s in self.stages.values():
            lines.append(f"{s.name:<24}{s.calls:>8d}{s.avg_ms:>10.2f}{s.max_ms:>10.2f}")
        lines.append(f"FPS: {self.fps():.1f}  Dropped: {self.dropped_frames}")
        return "\n".join(lines)
