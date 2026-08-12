"""High-concurrency allocation stress tests for leak detection."""
from __future__ import annotations

import gc
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

try:  # pragma: no cover - optional
    import tracemalloc  # stdlib, always present in 3.9+
    _TRACE = True
except Exception:  # pragma: no cover
    _TRACE = False


@dataclass
class LeakReport:
    iterations: int = 0
    concurrency: int = 0
    start_memory_kb: float = 0.0
    peak_memory_kb: float = 0.0
    end_memory_kb: float = 0.0
    leaked_kb: float = 0.0
    suspected_leak: bool = False


class MemoryLeakSimulator:
    """Stress-tests allocation-heavy code to detect leaks."""

    def stress(self, func: Callable[[], Any], iterations: int = 1000,
               concurrency: int = 10) -> LeakReport:
        report = LeakReport(iterations=iterations, concurrency=concurrency)
        gc.collect()
        start = self._current_kb()
        report.start_memory_kb = start
        peak = start

        if _TRACE:
            tracemalloc.start()

        def worker(n: int) -> None:
            nonlocal peak
            for _ in range(n):
                func()
                cur = self._current_kb()
                if cur > peak:
                    peak = cur

        per = max(1, iterations // concurrency)
        threads = [threading.Thread(target=worker, args=(per,)) for _ in range(concurrency)]
        t0 = time.perf_counter()
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        gc.collect()
        end = self._current_kb()
        report.peak_memory_kb = peak
        report.end_memory_kb = end
        report.leaked_kb = max(0.0, end - start)
        report.suspected_leak = report.leaked_kb > 1024  # >1MB sustained
        if _TRACE:
            tracemalloc.stop()
        return report

    def _current_kb(self) -> float:
        try:
            import resource
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        except Exception:
            return 0.0
