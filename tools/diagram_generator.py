"""Diagram generator: ASCII pipeline architecture flowcharts."""

from __future__ import annotations

from typing import List


class DiagramGenerator:
    """Render pipeline architectures as ASCII flowcharts."""

    @staticmethod
    def flowchart(stages: List[str], title: str = "Pipeline") -> str:
        if not stages:
            return f"{title}: (empty)"
        lines = [f"=== {title} ==="]
        for i, s in enumerate(stages):
            lines.append(f"  [{i}] {s}")
            if i < len(stages) - 1:
                lines.append("       |")
                lines.append("       v")
        return "\n".join(lines)

    @staticmethod
    def grid(blocks: List[List[str]]) -> str:
        rows = []
        for row in blocks:
            rows.append(" | ".join(row))
        return "\n".join(rows)
