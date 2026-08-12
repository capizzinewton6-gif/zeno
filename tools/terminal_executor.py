"""Safe, prompt-gated command execution engine.

A capability-style tool re-exporting terminal execution with explicit
confirmation gating for high-risk commands. Distinct from
``capabilities.terminal_execution`` which is the lower-level runner; this
module adds the interactive confirmation policy.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from capabilities.terminal_execution import CommandResult, TerminalExecution
from ai_core.safety_layer import SafetyLayer


@dataclass
class GatedCommand:
    command: str
    risk: str
    confirmed: bool = False


class TerminalExecutor:
    """Prompt-gated terminal executor for interactive use."""

    def __init__(self, terminal: TerminalExecution | None = None,
                 confirmer: Callable[[str, str], bool] | None = None) -> None:
        self.terminal = terminal or TerminalExecution()
        self.safety = self.terminal.safety
        self.confirmer = confirmer or self._default_confirmer

    def execute(self, command: str, auto_confirm: bool = False) -> CommandResult:
        decision = self.safety.check_command(command)
        if not decision:
            return CommandResult(command, -1, "", decision.reason,
                                 allowed=False, blocked_reason=decision.reason)
        if decision.risk_level in ("medium", "high") and not auto_confirm:
            confirmed = self.confirmer(command, decision.risk_level)
            if not confirmed:
                return CommandResult(command, -1, "",
                                     "User declined to confirm command.",
                                     allowed=False, blocked_reason="declined")
        return self.terminal.run(command, confirm=auto_confirm)

    def batch(self, commands: list[str], auto_confirm: bool = False) -> list[CommandResult]:
        return [self.execute(c, auto_confirm=auto_confirm) for c in commands]

    def _default_confirmer(self, command: str, risk: str) -> bool:
        # Non-interactive default: deny high-risk, allow medium
        return risk == "medium"
