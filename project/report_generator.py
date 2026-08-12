"""Generates development progress and code quality reports."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from calculations.complexity_metrics import ComplexityMetrics
from calculations.diff_stats import DiffAnalyzer
from config import load_json, memory_file
from project.task_manager import TaskManager


@dataclass
class ProgressReport:
    project: str
    generated_at: str
    tasks: dict[str, Any] = field(default_factory=dict)
    code_quality: dict[str, Any] = field(default_factory=dict)
    churn: dict[str, Any] = field(default_factory=dict)
    summary: str = ""


class ReportGenerator:
    """Assembles progress and quality reports."""

    def __init__(self, task_manager: TaskManager | None = None,
                 metrics: ComplexityMetrics | None = None) -> None:
        self.tasks = task_manager or TaskManager()
        self.metrics = metrics or ComplexityMetrics()
        self.diff = DiffAnalyzer()

    def progress(self, project_name: str = "") -> ProgressReport:
        task_progress = self.tasks.progress()
        report = ProgressReport(
            project=project_name,
            generated_at=datetime.now(timezone.utc).isoformat(),
            tasks=task_progress,
        )
        report.summary = (
            f"Tasks: {task_progress['done']}/{task_progress['total_tasks']} done "
            f"({task_progress['completion_pct']:.0f}%). "
            f"Open bugs: {task_progress['open_bugs']}."
        )
        return report

    def code_quality(self, sources: dict[str, str]) -> dict[str, Any]:
        """Compute aggregate quality metrics across files."""
        per_file: dict[str, Any] = {}
        total_complexity = 0.0
        for path, source in sources.items():
            cyclo = self.metrics.cyclomatic_complexity(source)
            halstead = self.metrics.halstead(source)
            total_complexity += cyclo
            per_file[path] = {
                "cyclomatic": cyclo,
                "halstead_volume": halstead["volume"],
                "lines": len(source.splitlines()),
            }
        return {
            "files": len(per_file),
            "avg_complexity": (total_complexity / len(per_file)) if per_file else 0.0,
            "per_file": per_file,
        }

    def changelog(self, diff: str) -> dict[str, Any]:
        stats = self.diff.analyze(diff)
        return {
            "additions": stats.additions,
            "deletions": stats.deletions,
            "files_changed": stats.files_changed,
            "impact": self.diff.impact_score(diff),
        }

    def to_markdown(self, report: ProgressReport) -> str:
        lines = [
            f"# Progress Report: {report.project}",
            f"_Generated: {report.generated_at}_",
            "",
            "## Summary",
            report.summary,
            "",
            "## Tasks",
            f"- Total: {report.tasks.get('total_tasks', 0)}",
            f"- Done: {report.tasks.get('done', 0)}",
            f"- Completion: {report.tasks.get('completion_pct', 0):.0f}%",
            f"- Open bugs: {report.tasks.get('open_bugs', 0)}",
        ]
        if report.code_quality:
            lines += ["", "## Code Quality",
                      f"- Files: {report.code_quality.get('files', 0)}",
                      f"- Avg complexity: {report.code_quality.get('avg_complexity', 0):.1f}"]
        return "\n".join(lines)
