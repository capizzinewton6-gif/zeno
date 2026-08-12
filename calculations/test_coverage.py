"""Line and branch coverage calculation mechanics."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CoverageReport:
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    files: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def line_coverage(self) -> float:
        return (self.covered_lines / self.total_lines * 100) if self.total_lines else 0.0

    @property
    def branch_coverage(self) -> float:
        return (self.covered_branches / self.total_branches * 100) if self.total_branches else 0.0


class CoverageCalculator:
    """Parses coverage.py-style output and computes coverage metrics."""

    def from_coverage_py(self, text: str) -> CoverageReport:
        """Parse `coverage report` text output."""
        report = CoverageReport()
        for line in text.splitlines():
            m = re.match(r"^(?P<file>\S+)\s+(?P<stmts>\d+)\s+(?P<miss>\d+)\s+(?P<cover>\d+)%", line)
            if m:
                stmts = int(m.group("stmts"))
                miss = int(m.group("miss"))
                covered = stmts - miss
                report.total_lines += stmts
                report.covered_lines += covered
                report.files[m.group("file")] = {
                    "statements": stmts, "missed": miss, "covered": covered}
        return report

    def estimate_branches(self, source: str, language: str = "python") -> int:
        """Estimate branch count from decision points in source."""
        import ast
        if language.lower() != "python":
            return len(re.findall(r"\b(if|for|while|switch|case|&&|\|\|)\b", source))
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return 0
        branches = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While)):
                branches += 2  # taken / not-taken
            elif isinstance(node, ast.BoolOp):
                branches += len(node.values) - 1
        return branches

    def merge(self, reports: list[CoverageReport]) -> CoverageReport:
        merged = CoverageReport()
        for r in reports:
            merged.total_lines += r.total_lines
            merged.covered_lines += r.covered_lines
            merged.total_branches += r.total_branches
            merged.covered_branches += r.covered_branches
            merged.files.update(r.files)
        return merged
