"""
actions - system_monitor
=========================
Monitor CPU, RAM, GPU, temperature and battery.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class SystemMonitor:
    """Monitor CPU, RAM, GPU, temperature and battery."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "system_monitor"
        self.description = "Monitor CPU, RAM, GPU, temperature and battery."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability."""
        # TODO: implement actions-specific logic
        return {"module": self.name, "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
