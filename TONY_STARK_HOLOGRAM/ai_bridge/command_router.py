"""
ai_bridge - command_router
========================================
Sends user commands to your AI.

Independent ai_bridge module for the Tony Stark Hologram OS.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class CommandRouter:
    """Sends user commands to your AI."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "command_router"
        self.description = "Sends user commands to your AI."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability (stub until hardware-backed)."""
        return {"module": self.name, "package": "ai_bridge", "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
