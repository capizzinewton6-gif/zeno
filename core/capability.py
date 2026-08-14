"""
core.capability - shared base class for all capabilities.

Every action / automation / agent / sensor / integration module implements the
same ``execute(task, context)`` contract. This base class centralises the
boilerplate (name, description, config, safe result helpers) so concrete
modules can focus on real logic instead of repeating the same stub skeleton.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


class Capability:
    """Base class for all capability modules.

    Subclasses set ``name`` and ``description`` (either as class attributes or
    in ``__init__``) and override :meth:`execute`. The registry auto-discovers
    modules by looking for the first user-defined class in each file, so every
    concrete capability must inherit from this base (or at least expose the
    same ``get_name`` / ``get_description`` / ``execute`` interface).
    """

    name: str = "capability"
    description: str = "Base capability."

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    # -- contract ----------------------------------------------------------

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task. Override in subclasses."""
        raise NotImplementedError

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def ok(message: str, **extra: Any) -> Dict[str, Any]:
        """Return a standard success result dict."""
        result: Dict[str, Any] = {"status": "ok", "result": message}
        result.update(extra)
        return result

    @staticmethod
    def error(message: str, **extra: Any) -> Dict[str, Any]:
        """Return a standard error result dict."""
        result: Dict[str, Any] = {"status": "error", "error": message}
        result.update(extra)
        return result

    @staticmethod
    def stub(task: str, name: str) -> Dict[str, Any]:
        """Return the legacy stub marker (for not-yet-implemented modules)."""
        return {"module": name, "task": task, "status": "stub"}

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{self.__class__.__name__} name={self.name!r}>"


def result_to_text(result: Any) -> str:
    """Flatten a capability result into a human-readable string."""
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if "result" in result:
            base = str(result["result"])
        elif "error" in result:
            base = f"error: {result['error']}"
        elif "status" in result:
            base = str(result["status"])
        else:
            base = json.dumps(result, default=str)
        return base
    if isinstance(result, (list, tuple)):
        return "\n".join(result_to_text(item) for item in result)
    return str(result)
