"""Safeguards preventing destructive file or terminal operations.

Acts as the enforcement gate before any mutating capability executes. Every
write, delete, or shell command must pass through this layer.
"""
from __future__ import annotations

import fnmatch
import os
import shlex
from dataclasses import dataclass, field
from typing import Any

from config import get_settings

# Filesystem guards ---------------------------------------------------------
PROTECTED_PATHS = (
    "/", "/etc", "/usr", "/bin", "/sbin", "/boot", "/dev", "/proc",
    "/sys", "/root", os.path.expanduser("~/.ssh"),
    os.path.expanduser("~/.config"),
)

# Forbidden command patterns (substring match, case-insensitive)
FORBIDDEN_PATTERNS = (
    "rm -rf /", "rm -rf /*", "rm -fr /", "mkfs", "dd if=/dev/",
    ":(){ :|:&", "shutdown", "reboot", "halt", "init 0", "init 6",
    "> /dev/sd", "chmod -R 777 /", "chown -R", "curl | sh", "wget | sh",
    "curl | bash", "wget | bash", "mv / ", "cp /dev/zero",
)


@dataclass
class SafetyDecision:
    allowed: bool
    reason: str = ""
    risk_level: str = "low"  # low, medium, high
    suggestions: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.allowed


class SafetyLayer:
    """Central guard for destructive operations."""

    def __init__(self) -> None:
        self._settings = get_settings().get("sandbox", {})
        self._forbidden = set(self._settings.get(
            "forbidden_commands", list(FORBIDDEN_PATTERNS)))
        self._confirmations: dict[str, bool] = {}

    # -- Filesystem ----------------------------------------------------------
    def check_write(self, path: str, content: str | bytes | None = None) -> SafetyDecision:
        abs_path = os.path.abspath(path)
        for protected in PROTECTED_PATHS:
            if abs_path == protected or abs_path.startswith(protected.rstrip("/") + "/"):
                if abs_path != os.getcwd():
                    return SafetyDecision(
                        False, f"Refused: {abs_path} is a protected system path.",
                        "high", ["Target a path inside the project workspace."])

        # Block writes to secrets-bearing files
        name = os.path.basename(abs_path).lower()
        if name in {".env", "credentials", "secrets.json"} or "secret" in name:
            return SafetyDecision(
                False, f"Refused: {abs_path} looks like a secrets file.",
                "high", ["Move secrets to a non-tracked, permissioned location."])

        return SafetyDecision(True, "ok", "low")

    def check_delete(self, path: str) -> SafetyDecision:
        abs_path = os.path.abspath(path)
        for protected in PROTECTED_PATHS:
            if abs_path.startswith(protected.rstrip("/") + "/") or abs_path == protected:
                return SafetyDecision(
                    False, f"Refused delete on protected path {abs_path}.", "high")
        if abs_path == os.getcwd() or abs_path == os.path.expanduser("~"):
            return SafetyDecision(
                False, "Refused: cannot delete workspace or home root.", "high")
        return SafetyDecision(True, "ok", "medium")

    # -- Terminal ------------------------------------------------------------
    def check_command(self, command: str) -> SafetyDecision:
        cmd = command.strip()
        lowered = cmd.lower()
        for pat in self._forbidden:
            if pat.lower() in lowered:
                return SafetyDecision(
                    False, f"Refused: command matches forbidden pattern '{pat}'.", "high",
                    ["Restrict the command to the workspace."])

        # Detect pipe-to-shell from network
        if ("curl" in lowered or "wget" in lowered) and ("| sh" in lowered or "| bash" in lowered):
            return SafetyDecision(
                False, "Refused: pipe-to-shell from network fetch.", "high",
                ["Download, inspect, then execute explicitly."])

        # Detect backgrounded destructive commands
        if cmd.endswith("&") and any(k in lowered for k in ("rm ", "dd ", "mkfs")):
            return SafetyDecision(
                False, "Refused: destructive backgrounded command.", "high")

        # Risk profiling
        risk = "low"
        if any(k in lowered for k in ("rm ", "mv ", "chmod", "chown", "dd ", "sudo")):
            risk = "medium"
        if "sudo" in lowered:
            risk = "high"

        return SafetyDecision(True, "allowed", risk)

    # -- Confirmation gate ---------------------------------------------------
    def request_confirmation(self, action: str, detail: str) -> SafetyDecision:
        """Return a decision requiring human confirmation for high-risk actions."""
        return SafetyDecision(
            False, f"Confirmation required for {action}: {detail}", "high",
            [f"Confirm the {action} explicitly to proceed."])

    def grant(self, token: str) -> None:
        """Mark a one-shot confirmation token as granted."""
        self._confirmations[token] = True

    def is_granted(self, token: str) -> bool:
        return self._confirmations.pop(token, False)
