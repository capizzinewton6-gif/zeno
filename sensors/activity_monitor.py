"""
sensors - activity_monitor
===========================
Track app and website usage.

Independent sensors module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class ActivityMonitor:
    """Track app and website usage."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "activity_monitor"
        self.description = "Track app and website usage."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability."""
        # TODO: implement sensors-specific logic
        return {"module": self.name, "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
