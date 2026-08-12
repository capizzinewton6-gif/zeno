"""Visual heatmaps for unit test code coverage."""
from __future__ import annotations

from typing import Any

from calculations.test_coverage import CoverageReport


class CoverageVisualizer:
    """Renders coverage reports as text heatmaps."""

    def heatmap(self, report: CoverageReport, source: str = "",
                covered_lines: set[int] | None = None) -> str:
        if not source:
            return self._summary(report)
        covered = covered_lines or set()
        out: list[str] = [self._summary(report), "", "Line coverage:"]
        for i, line in enumerate(source.splitlines(), 1):
            mark = "✓" if i in covered else "✗"
            color = "\033[32m" if i in covered else "\033[31m"
            reset = "\033[0m"
            out.append(f"{color}{mark}{reset} {i:>4} │ {line}")
        return "\n".join(out)

    def file_heatmap(self, files: dict[str, dict[str, int]]) -> str:
        lines: list[str] = ["Coverage by file:"]
        for path, stats in files.items():
            pct = (stats["covered"] / stats["statements"] * 100) if stats["statements"] else 0
            bar = self._bar(pct)
            lines.append(f"  {path:<40} {bar} {pct:5.1f}%")
        return "\n".join(lines)

    def _summary(self, report: CoverageReport) -> str:
        return (f"Line coverage: {report.line_coverage:.1f}% "
                f"({report.covered_lines}/{report.total_lines}) | "
                f"Branch coverage: {report.branch_coverage:.1f}%")

    def _bar(self, pct: float, width: int = 20) -> str:
        filled = int(pct / 100 * width)
        return "[" + "█" * filled + "░" * (width - filled) + "]"
