"""Base class for language engines."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer
from config import tool_path
from modeling.coding_rules import RuleSet, ruleset_for


@dataclass
class LintResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fixable: int = 0


@dataclass
class ExecResult:
    ok: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float = 0.0


class LanguageEngine:
    """Base for per-language toolchains."""

    name: str = "base"
    extensions: tuple[str, ...] = ()

    def __init__(self, safety: SafetyLayer | None = None) -> None:
        self.safety = safety or SafetyLayer()

    @property
    def rules(self) -> RuleSet:
        return ruleset_for(self.name)

    def is_available(self) -> bool:
        """Whether the primary toolchain binary is on PATH."""
        return any(self._bin(b) for b in self.required_tools())

    def required_tools(self) -> list[str]:
        return []

    def lint(self, path: str) -> LintResult:
        raise NotImplementedError

    def format(self, path: str) -> LintResult:
        raise NotImplementedError

    def run(self, path: str) -> ExecResult:
        raise NotImplementedError

    def _bin(self, name: str) -> str | None:
        return tool_path(name)

    def _exec(self, command: str, cwd: str | None = None) -> ExecResult:
        import subprocess
        import time
        decision = self.safety.check_command(command)
        if not decision:
            return ExecResult(False, -1, "", decision.reason)
        start = time.perf_counter()
        try:
            proc = subprocess.run(command, shell=True, cwd=cwd,
                                  capture_output=True, text=True, timeout=120)
            return ExecResult(proc.returncode == 0, proc.returncode,
                              proc.stdout, proc.stderr,
                              (time.perf_counter() - start) * 1000)
        except subprocess.TimeoutExpired:
            return ExecResult(False, -1, "", "timeout")
        except Exception as exc:
            return ExecResult(False, -1, "", str(exc))
