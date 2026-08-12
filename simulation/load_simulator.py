"""Benchmark load testing for generated APIs."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

try:  # pragma: no cover - optional
    import requests  # type: ignore
    _REQUESTS = True
except Exception:  # pragma: no cover
    _REQUESTS = False


@dataclass
class LoadResult:
    url: str
    total_requests: int = 0
    successful: int = 0
    failed: int = 0
    duration_s: float = 0.0
    rps: float = 0.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    errors: list[str] = field(default_factory=list)


class LoadSimulator:
    """Simple concurrent load tester for HTTP endpoints."""

    def __init__(self) -> None:
        if not _REQUESTS:
            self._note = "requests not installed; load testing unavailable"

    def load_test(self, url: str, concurrency: int = 10, duration_s: int = 10,
                  method: str = "GET", payload: dict | None = None) -> LoadResult:
        result = LoadResult(url=url)
        if not _REQUESTS:
            result.errors.append("requests not installed")
            return result

        import concurrent.futures

        latencies: list[float] = []
        end_time = time.time() + duration_s

        def worker() -> None:
            while time.time() < end_time:
                start = time.perf_counter()
                try:
                    if method == "GET":
                        resp = requests.get(url, timeout=5)
                    else:
                        resp = requests.post(url, json=payload, timeout=5)
                    lat = (time.perf_counter() - start) * 1000
                    latencies.append(lat)
                    if 200 <= resp.status_code < 300:
                        result.successful += 1
                    else:
                        result.failed += 1
                        if len(result.errors) < 20:
                            result.errors.append(f"HTTP {resp.status_code}")
                except Exception as exc:
                    result.failed += 1
                    if len(result.errors) < 20:
                        result.errors.append(str(exc)[:100])
                result.total_requests += 1

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(worker) for _ in range(concurrency)]
            concurrent.futures.wait(futures)
        result.duration_s = time.time() - start
        result.rps = result.total_requests / result.duration_s if result.duration_s else 0
        if latencies:
            result.avg_latency_ms = sum(latencies) / len(latencies)
            sl = sorted(latencies)
            result.p95_latency_ms = sl[int(len(sl) * 0.95)] if sl else 0
        return result
