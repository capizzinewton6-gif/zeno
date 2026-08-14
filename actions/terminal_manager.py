"""
actions - terminal_manager
===========================
Run shell, bash and powershell commands.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import shlex
import subprocess
from typing import Any, Dict, Optional

from core.capability import Capability


class TerminalManager(Capability):
    """Run shell, bash and powershell commands."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "terminal_manager"
        self.description = "Run shell, bash and powershell commands."
        self.timeout = int(self.config.get("timeout", 30))
        # Commands that mutate the system destructively and require confirmation.
        self.dangerous = ("rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", "shutdown", "reboot")

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a shell command described by ``task``."""
        command = self._extract_command(task)
        if not command:
            return self.error("No command found in task.")
        if command.strip().startswith(self.dangerous):
            return self.error(f"Blocked dangerous command: {command}")

        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            output = (proc.stdout or "") + (proc.stderr or "")
            output = output.strip()
            if proc.returncode == 0:
                return self.ok(output or "(no output)", command=command, returncode=proc.returncode)
            return self.error(output or f"exit code {proc.returncode}", command=command, returncode=proc.returncode)
        except subprocess.TimeoutExpired:
            return self.error(f"Command timed out after {self.timeout}s", command=command)
        except Exception as exc:
            return self.error(str(exc), command=command)

    def _extract_command(self, task: str) -> str:
        """Pull the actual command out of a natural-language task string."""
        task = task.strip()
        # Strip common leading phrases.
        for prefix in ("run command:", "run:", "terminal:", "shell:", "bash:", "execute:"):
            if task.lower().startswith(prefix):
                task = task[len(prefix):].strip()
        # If quoted, use the quoted portion.
        if (task.startswith('"') and '"' in task[1:]) or (task.startswith("'") and "'" in task[1:]):
            try:
                return shlex.split(task)[0]
            except ValueError:
                pass
        return task
