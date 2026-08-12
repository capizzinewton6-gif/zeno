"""
interaction - voice_interface
========================================
Sends voice commands to existing AI.

Independent interaction module for the Tony Stark Hologram OS.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class VoiceInterface:
    """Sends voice commands to existing AI."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "voice_interface"
        self.description = "Sends voice commands to existing AI."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability (stub until hardware-backed)."""
        return {"module": self.name, "package": "interaction", "task": task, "status": "stub"}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
