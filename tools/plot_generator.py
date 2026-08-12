"""Performance and memory profile plotting tools."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from calculations.performance_profiler import BenchmarkResult, BigOEstimate


@dataclass
class PlotData:
    title: str
    x_label: str
    y_label: str
    series: list[dict[str, Any]] = field(default_factory=list)


class PlotGenerator:
    """Produces ASCII plots (and matplotlib data) for profiles."""

    def bigo_plot(self, estimate: BigOEstimate) -> str:
        if not estimate.samples:
            return f"{estimate.complexity} (no samples)"
        max_n = max(n for n, _ in estimate.samples)
        max_t = max(t for _, t in estimate.samples) or 1.0
        lines = [f"Big-O: {estimate.complexity} (conf {estimate.confidence})",
                 f"{'n':>10} {'time(ms)':>10} {'bar':<40}"]
        for n, t in estimate.samples:
            bar = "█" * int(t / max_t * 40)
            lines.append(f"{n:>10} {t:>10.3f} {bar}")
        return "\n".join(lines)

    def benchmark_plot(self, result: BenchmarkResult) -> str:
        lines = [f"{result.name} ({result.runs} runs)",
                 f"mean: {result.mean_ms:.3f}ms  min: {result.min_ms:.3f}ms  "
                 f"max: {result.max_ms:.3f}ms  std: {result.std_ms:.3f}ms"]
        return "\n".join(lines)

    def series_plot(self, data: PlotData) -> str:
        lines = [f"{data.title}", f"{data.x_label} vs {data.y_label}"]
        all_points = [(p["x"], p["y"]) for s in data.series for p in s.get("points", [])]
        if not all_points:
            return "\n".join(lines) + "\n(no data)"
        max_y = max(y for _, y in all_points) or 1.0
        for series in data.series:
            lines.append(f"  {series.get('label', 'series')}:")
            for x, y in series.get("points", []):
                bar = "█" * int(y / max_y * 30)
                lines.append(f"    {x:>8} {bar} {y}")
        return "\n".join(lines)

    def to_matplotlib(self, data: PlotData) -> dict[str, Any]:  # pragma: no cover
        return {
            "title": data.title, "xlabel": data.x_label, "ylabel": data.y_label,
            "series": [{"label": s.get("label", ""), "points": s.get("points", [])}
                       for s in data.series],
        }
