"""Codebase churn, bug density, and module complexity analysis."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from calculations.complexity_metrics import ComplexityMetrics
from calculations.diff_stats import DiffAnalyzer
from repository_workspace.git_interface import GitInterface


@dataclass
class ModuleComplexity:
    file: str
    complexity: float
    lines: int
    complexity_per_line: float


@dataclass
class CodebaseAnalysis:
    total_files: int = 0
    total_lines: int = 0
    avg_complexity: float = 0.0
    hotspots: list[ModuleComplexity] = field(default_factory=list)
    churn: dict[str, Any] = field(default_factory=dict)
    bug_density: dict[str, float] = field(default_factory=dict)


class DataAnalyzer:
    """Analyzes codebase-wide metrics."""

    def __init__(self, metrics: ComplexityMetrics | None = None,
                 git: GitInterface | None = None) -> None:
        self.metrics = metrics or ComplexityMetrics()
        self.git = git or GitInterface()
        self.diff = DiffAnalyzer()

    def analyze(self, root: str | Path, language: str = "python") -> CodebaseAnalysis:
        root_path = Path(root)
        analysis = CodebaseAnalysis()
        ext_map = {"python": ".py", "javascript": ".js", "typescript": ".ts",
                   "rust": ".rs", "go": ".go"}
        ext = ext_map.get(language, ".py")
        complexities: list[ModuleComplexity] = []
        for p in root_path.rglob(f"*{ext}"):
            if any(part in {"node_modules", "__pycache__", ".git", "venv", ".venv"}
                   for part in p.parts):
                continue
            try:
                source = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            cyclo = self.metrics.cyclomatic_complexity(source, language)
            lines = len(source.splitlines())
            complexities.append(ModuleComplexity(
                file=str(p.relative_to(root_path)),
                complexity=cyclo, lines=lines,
                complexity_per_line=round(cyclo / max(1, lines), 3)))
            analysis.total_files += 1
            analysis.total_lines += lines

        analysis.avg_complexity = (
            sum(c.complexity for c in complexities) / len(complexities)
            if complexities else 0.0
        )
        analysis.hotspots = sorted(complexities,
                                   key=lambda c: c.complexity_per_line,
                                   reverse=True)[:10]
        return analysis

    def churn_analysis(self, since: str = "HEAD~10") -> dict[str, Any]:
        """Aggregate churn from git history."""
        res = self.git._git(f"log --oneline {since}..HEAD")
        commits = res.stdout.count("\n") if res.ok else 0
        diff_res = self.git._git(f"diff --stat {since}..HEAD")
        stats = self.diff.analyze(diff_res.stdout) if diff_res.ok else None
        return {
            "commits": commits,
            "additions": stats.additions if stats else 0,
            "deletions": stats.deletions if stats else 0,
            "files_changed": stats.files_changed if stats else 0,
        }

    def bug_density(self, files: list[str], bug_counts: dict[str, int]) -> dict[str, float]:
        """Compute bugs-per-KLOC per file."""
        out: dict[str, float] = {}
        for f in files:
            p = Path(f)
            try:
                lines = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
            except OSError:
                continue
            bugs = bug_counts.get(f, 0)
            out[f] = round(bugs / max(1, lines / 1000), 3)
        return out
