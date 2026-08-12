"""Safe local terminal command runner and output parser.

A capability module that executes shell commands in the local workspace,
subject to the safety layer's approval and the configured sandbox limits.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from typing import Any

from ai_core.safety_layer import SafetyLayer, SafetyDecision
from config import get_settings


@dataclass
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float = 0.0
    allowed: bool = True
    blocked_reason: str = ""

    @property
    def ok(self) -> bool:
        return self.allowed and self.exit_code == 0


class TerminalExecution:
    """Capability: run commands safely in the local workspace."""

    def __init__(self, safety: SafetyLayer | None = None,
                 workspace: str | None = None) -> None:
        self.safety = safety or SafetyLayer()
        self.workspace = workspace or os.getcwd()
        self._settings = get_settings().get("sandbox", {})
        self._timeout = self._settings.get("timeout_seconds", 30)
        self._max_bytes = self._settings.get("max_output_bytes", 1_048_576)

    def run(self, command: str, *, timeout: int | None = None,
            env: dict[str, str] | None = None,
            confirm: bool = False) -> CommandResult:
        decision = self.safety.check_command(command)
        if not decision:
            return CommandResult(command, -1, "", decision.reason,
                                 allowed=False, blocked_reason=decision.reason)
        if decision.risk_level == "high" and not confirm:
            return CommandResult(
                command, -1, "",
                f"High-risk command requires explicit confirmation: {decision.reason}",
                allowed=False, blocked_reason="needs confirmation")

        try:
            proc_env = os.environ.copy()
            if env:
                proc_env.update(env)
            proc = subprocess.run(
                command, shell=True, cwd=self.workspace,
                capture_output=True, text=True, timeout=timeout or self._timeout,
                env=proc_env,
            )
            stdout = self._truncate(proc.stdout)
            stderr = self._truncate(proc.stderr)
            return CommandResult(command, proc.returncode, stdout, stderr)
        except subprocess.TimeoutExpired:
            return CommandResult(command, -1, "", f"Command timed out after {timeout or self._timeout}s")
        except Exception as exc:
            return CommandResult(command, -1, "", f"Execution error: {exc}")

    def run_many(self, commands: list[str]) -> list[CommandResult]:
        return [self.run(c) for c in commands]

    def _truncate(self, text: str) -> str:
        if len(text.encode("utf-8")) > self._max_bytes:
            return text[: self._max_bytes // 4] + "\n...[truncated]"
        return text

    def parse_output(self, result: CommandResult, marker: str = "ERROR") -> list[str]:
        """Extract lines containing a marker (e.g. error lines) from output."""
        hay = f"{result.stdout}\n{result.stderr}"
        return [line for line in hay.splitlines() if marker.lower() in line.lower()]
