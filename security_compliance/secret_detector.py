"""Scans for leaked credentials, API keys, and private keys."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SecretFinding:
    type: str
    line: int
    match: str  # masked
    confidence: float


@dataclass
class SecretReport:
    findings: list[SecretFinding] = field(default_factory=list)
    scanned_files: int = 0

    @property
    def has_high_confidence(self) -> bool:
        return any(f.confidence >= 0.8 for f in self.findings)


class SecretDetector:
    """Regex-based secret detection across source files."""

    PATTERNS: list[dict[str, Any]] = [
        {"type": "AWS Access Key", "regex": r"AKIA[0-9A-Z]{16}", "confidence": 0.95},
        {"type": "AWS Secret", "regex": r"(?i)aws(.{0,20})?(secret|sk)[^\n]{0,5}['\"][0-9a-zA-Z/+=]{40}['\"]", "confidence": 0.8},
        {"type": "Google API Key", "regex": r"AIza[0-9A-Za-z\-_]{35}", "confidence": 0.95},
        {"type": "GitHub Token", "regex": r"gh[pousr]_[0-9A-Za-z]{36}", "confidence": 0.95},
        {"type": "Slack Token", "regex": r"xox[baprs]-[0-9A-Za-z-]{10,}", "confidence": 0.9},
        {"type": "Private Key", "regex": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "confidence": 1.0},
        {"type": "JWT", "regex": r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "confidence": 0.85},
        {"type": "Generic API Key", "regex": r"(?i)(api[_-]?key|secret|token)[\s:=]{1,4}['\"][0-9a-zA-Z]{16,}['\"]", "confidence": 0.6},
        {"type": "Connection String", "regex": r"(?:mongodb|postgres|mysql|redis)://[^\s'\"]+:[^\s'\"]+@", "confidence": 0.85},
    ]

    def scan(self, source: str) -> SecretReport:
        report = SecretReport()
        lines = source.splitlines()
        for pat in self.PATTERNS:
            for i, line in enumerate(lines, 1):
                for m in re.finditer(pat["regex"], line):
                    report.findings.append(SecretFinding(
                        type=pat["type"], line=i,
                        match=self._mask(m.group()), confidence=pat["confidence"]))
        return report

    def scan_file(self, path: str) -> SecretReport:
        try:
            with open(path, encoding="utf-8") as f:
                return self.scan(f.read())
        except OSError:
            return SecretReport()

    def _mask(self, s: str) -> str:
        if len(s) <= 8:
            return "*" * len(s)
        return s[:4] + "*" * (len(s) - 8) + s[-4:]
