"""Identifies SQL injection, XSS, and command injection risks.

A focused input-validation analyzer that flags unsanitized flows into dangerous
sinks. Complements the broader SAST scanner with taint-style heuristics.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InjectionRisk:
    kind: str  # sqli, xss, command-injection
    line: int
    sink: str
    evidence: str
    severity: str = "high"


@dataclass
class SanitizerReport:
    risks: list[InjectionRisk] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)  # untrusted input sources


class InputSanitizer:
    """Heuristic taint analysis for injection risks."""

    INPUT_SOURCES = {
        "python": [r"request\.(?:GET|POST|args|form|json|data|values|cookies)",
                   r"input\s*\(", r"sys\.argv", r"os\.environ",
                   r"flask\.request", r"fastapi\..*Query"],
    }

    SINKS = {
        "python": [
            ("sqli", r"\.execute\s*\([^)]*\+[^)]*\)"),
            ("sqli", r"\.execute\s*\([^)]*%[^)]*\)"),
            ("sqli", r"\.execute\s*\([^)]*format\("),
            ("command-injection", r"subprocess\.(?:run|call|Popen)\s*\([^)]*shell\s*=\s*True"),
            ("command-injection", r"os\.system\s*\("),
            ("xss", r"(?:render_template_string|innerHTML)\s*\([^)]*%[^)]*\)"),
        ],
    }

    def analyze(self, source: str, language: str = "python") -> SanitizerReport:
        report = SanitizerReport()
        if language.lower() not in self.INPUT_SOURCES:
            return report
        lines = source.splitlines()
        # detect sources
        for pat in self.INPUT_SOURCES[language]:
            for i, line in enumerate(lines, 1):
                if re.search(pat, line):
                    report.sources.append(f"line {i}: {line.strip()[:60]}")
        # detect sinks
        for kind, pat in self.SINKS[language]:
            for i, line in enumerate(lines, 1):
                if re.search(pat, line):
                    report.risks.append(InjectionRisk(
                        kind=kind, line=i, sink=pat[:30],
                        evidence=line.strip()[:80]))
        return report

    def suggest_fix(self, risk: InjectionRisk, language: str = "python") -> str:
        if risk.kind == "sqli":
            return "Use parameterized queries: cursor.execute(sql, (params,))"
        if risk.kind == "command-injection":
            return "Use shell=False and pass args as a list; validate inputs."
        if risk.kind == "xss":
            return "Escape output; use templating with autoescaping."
        return "Validate and sanitize all untrusted input."
