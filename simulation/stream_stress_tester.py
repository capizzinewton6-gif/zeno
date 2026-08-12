"""Multi-camera concurrent stream throughput testing."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from calculations.latency_metrics import LatencyMetrics


@dataclass
class StreamResult:
    name: str
    frames_processed: int = 0
    fps: float = 0.0
    errors: int = 0
    metrics: LatencyMetrics = field(default_factory=LatencyMetrics)


class StreamStressTester:
    """Run N synthetic/camera streams concurrently and report throughput."""

    def __init__(self, duration_s: float = 10.0) -> None:
        self.duration_s = duration_s
        self.results: Dict[str, StreamResult] = {}

    def run(self, streams: Dict[str, Callable]) -> Dict[str, StreamResult]:
        threads = []
        stop = threading.Event()

        def worker(name: str, next_frame: Callable):
            res = self.results.setdefault(name, StreamResult(name=name))
            start = time.time()
            while not stop.is_set() and (time.time() - start) < self.duration_s:
                try:
                    frame = next_frame()
                    if frame is None:
                        break
                    res.frames_processed += 1
                    res.metrics.tick()
                except Exception:
                    res.errors += 1
            res.fps = res.frames_processed / max(time.time() - start, 1e-6)

        for name, stream in streams.items():
            t = threading.Thread(target=worker, args=(name, stream))
            t.start()
            threads.append(t)
        time.sleep(self.duration_s)
        stop.set()
        for t in threads:
            t.join(timeout=2.0)
        return self.results

    def summary(self) -> str:
        lines = [f"{'Stream':<16}{'Frames':>8}{'FPS':>8}{'Errors':>8}"]
        for r in self.results.values():
            lines.append(f"{r.name:<16}{r.frames_processed:>8d}{r.fps:>8.1f}{r.errors:>8d}")
        return "\n".join(lines)
