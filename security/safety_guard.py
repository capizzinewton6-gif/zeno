"""
security - safety_guard
========================
Block dangerous actions.

Independent security module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class SafetyGuard:
    """Block dangerous actions."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "safety_guard"
        self.description = "Block dangerous actions."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability."""
        # TODO: implement security-specific logic
        return {"module": self.name, "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
