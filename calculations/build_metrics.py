"""Compilation speed, memory footprint, and binary size stats."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class BuildMetric:
    name: str
    duration_ms: float = 0.0
    binary_size_bytes: int = 0
    peak_memory_bytes: int = 0
    success: bool = False
    output: str = ""


class BuildMetrics:
    """Measure build performance for compiled artifacts."""

    def measure_binary(self, path: str | Path) -> int:
        p = Path(path)
        return p.stat().st_size if p.exists() else 0

    def time_build(self, command: str, cwd: str | None = None) -> BuildMetric:
        import subprocess
        start = time.perf_counter()
        try:
            proc = subprocess.run(command, shell=True, cwd=cwd,
                                  capture_output=True, text=True, timeout=600)
            duration = (time.perf_counter() - start) * 1000
            return BuildMetric(
                name=command, duration_ms=duration,
                success=proc.returncode == 0,
                output=proc.stdout[-2000:] + proc.stderr[-2000:],
            )
        except Exception as exc:
            return BuildMetric(name=command, success=False, output=str(exc))

    def human_size(self, n: int) -> str:
        from calculations.unit_converter import human_bytes
        return human_bytes(n)
