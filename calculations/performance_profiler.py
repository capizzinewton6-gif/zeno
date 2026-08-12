"""Execution time benchmarking and Big-O estimation."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from calculations.complexity_metrics import ComplexityMetrics


@dataclass
class BenchmarkResult:
    name: str
    runs: int
    total_ms: float
    mean_ms: float
    min_ms: float
    max_ms: float
    std_ms: float = 0.0


@dataclass
class BigOEstimate:
    complexity: str  # O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n)
    confidence: float
    samples: list[tuple[int, float]] = field(default_factory=list)


class PerformanceProfiler:
    """Benchmarks functions and estimates Big-O complexity."""

    def __init__(self, metrics: ComplexityMetrics | None = None) -> None:
        self.metrics = metrics or ComplexityMetrics()

    def benchmark(self, func: Callable[..., Any], args_factory: Callable[[int], tuple],
                  sizes: list[int] | None = None, runs: int = 5) -> BenchmarkResult:
        sizes = sizes or [1]
        times: list[float] = []
        for _ in range(runs):
            args = args_factory(sizes[0])
            start = time.perf_counter()
            func(*args)
            times.append((time.perf_counter() - start) * 1000)
        return BenchmarkResult(
            name=getattr(func, "__name__", "func"), runs=runs,
            total_ms=sum(times), mean_ms=sum(times) / len(times),
            min_ms=min(times), max_ms=max(times),
            std_ms=self._std(times),
        )

    def estimate_bigo(self, func: Callable[..., Any],
                      args_factory: Callable[[int], tuple],
                      sizes: list[int] | None = None) -> BigOEstimate:
        sizes = sorted(sizes or [10, 100, 1000, 10000])
        samples: list[tuple[int, float]] = []
        for n in sizes:
            args = args_factory(n)
            start = time.perf_counter()
            func(*args)
            samples.append((n, (time.perf_counter() - start) * 1000))
        return self._classify_bigo(samples)

    def _classify_bigo(self, samples: list[tuple[int, float]]) -> BigOEstimate:
        if len(samples) < 2:
            return BigOEstimate("O(1)", 0.0, samples)
        n0, t0 = samples[0]
        n1, t1 = samples[-1]
        if n0 == 0 or t0 == 0:
            return BigOEstimate("O(?)", 0.0, samples)
        ratio = (t1 / max(t0, 1e-9))
        size_ratio = n1 / max(n0, 1)
        log_ratio = _safe_log(size_ratio)
        # Compare growth ratio to known complexities
        candidates = {
            "O(1)": 1.0,
            "O(log n)": log_ratio,
            "O(n)": size_ratio,
            "O(n log n)": size_ratio * max(1, log_ratio),
            "O(n^2)": size_ratio ** 2,
            "O(2^n)": 2 ** size_ratio if size_ratio < 30 else float("inf"),
        }
        best = min(candidates, key=lambda k: abs(_safe_log(max(candidates[k], 1e-9)) - _safe_log(max(ratio, 1e-9))))
        confidence = max(0.0, 1.0 - abs(_safe_log(max(candidates[best], 1e-9)) - _safe_log(max(ratio, 1e-9))))
        return BigOEstimate(best, round(confidence, 2), samples)

    def _std(self, xs: list[float]) -> float:
        if len(xs) < 2:
            return 0.0
        mean = sum(xs) / len(xs)
        return (sum((x - mean) ** 2 for x in xs) / len(xs)) ** 0.5


def _safe_log(n: float) -> float:
    import math
    return math.log(n) if n > 0 else 0.0
