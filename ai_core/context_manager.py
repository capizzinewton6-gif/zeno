"""Active physical system context: degrees of freedom and constraints."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class SystemContext:
    name: str = ""
    regime: str = "classical"
    degrees_of_freedom: list[str] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    parameters: dict[str, float] = field(default_factory=dict)
    unit_system: str = "SI"
    notes: str = ""

    def set_state(self, key: str, value: Any) -> None:
        self.state[key] = value

    def add_constraint(self, constraint: str) -> None:
        self.constraints.append(constraint)

    def set_parameter(self, name: str, value: float) -> None:
        self.parameters[name] = value

    def snapshot(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "regime": self.regime,
            "degrees_of_freedom": list(self.degrees_of_freedom),
            "state": dict(self.state),
            "constraints": list(self.constraints),
            "parameters": dict(self.parameters),
            "unit_system": self.unit_system,
        }


class ContextManager:
    """Holds the currently active physical system for an agent run."""

    def __init__(self):
        self._stack: list[SystemContext] = []

    @property
    def current(self) -> Optional[SystemContext]:
        return self._stack[-1] if self._stack else None

    def push(self, ctx: SystemContext) -> SystemContext:
        self._stack.append(ctx)
        return ctx

    def pop(self) -> Optional[SystemContext]:
        return self._stack.pop() if self._stack else None

    def reset(self) -> None:
        self._stack.clear()


CONTEXT = ContextManager()
