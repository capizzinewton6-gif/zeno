"""
hardware - projector_controller
========================================
Projection hardware interface.

Independent hardware module for the Tony Stark Hologram OS.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class ProjectorController:
    """Projection hardware interface."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "projector_controller"
        self.description = "Projection hardware interface."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability (stub until hardware-backed)."""
        return {"module": self.name, "package": "hardware", "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
