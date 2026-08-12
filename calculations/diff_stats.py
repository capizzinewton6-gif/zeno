"""Code churn, lines added/deleted, and file impact scoring."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DiffStats:
    additions: int = 0
    deletions: int = 0
    files_changed: int = 0
    files: list[dict[str, int]] = field(default_factory=list)

    @property
    def churn(self) -> int:
        return self.additions + self.deletions

    @property
    def net(self) -> int:
        return self.additions - self.deletions


class DiffAnalyzer:
    """Parse unified diffs and compute churn/impact metrics."""

    def analyze(self, diff: str) -> DiffStats:
        additions = deletions = 0
        current_file: str | None = None
        file_stats: dict[str, dict[str, int]] = {}
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
                file_stats.setdefault(current_file, {"additions": 0, "deletions": 0})
            elif line.startswith("+++") or line.startswith("---"):
                continue
            elif line.startswith("+") and not line.startswith("+++"):
                additions += 1
                if current_file:
                    file_stats[current_file]["additions"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1
                if current_file:
                    file_stats[current_file]["deletions"] += 1
        files = [{"file": f, **s} for f, s in file_stats.items()]
        return DiffStats(additions=additions, deletions=deletions,
                         files_changed=len(file_stats), files=files)

    def impact_score(self, diff: str) -> float:
        """Higher = more impactful change. Combines churn and file spread."""
        stats = self.analyze(diff)
        spread = stats.files_changed
        return round(stats.churn * (1 + 0.1 * spread), 1)

    def hotspots(self, diff: str, top: int = 5) -> list[dict[str, Any]]:
        stats = self.analyze(diff)
        ranked = sorted(stats.files, key=lambda f: f["additions"] + f["deletions"], reverse=True)
        return ranked[:top]
