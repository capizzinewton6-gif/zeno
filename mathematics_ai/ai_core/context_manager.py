"""Context manager for mathematical problems and domain context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProblemContext:
    statement: str
    domain: str = "unknown"
    assumptions: list[str] = field(default_factory=list)
    symbols: dict[str, str] = field(default_factory=dict)
    precision: int = 50
    history: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_assumption(self, assumption: str) -> None:
        self.assumptions.append(assumption)

    def define_symbol(self, name: str, meaning: str) -> None:
        self.symbols[name] = meaning

    def record(self, action: str, result: Any) -> None:
        self.history.append({"action": action, "result": result})

    def summary(self) -> str:
        lines = [f"Domain: {self.domain}", f"Statement: {self.statement}"]
        if self.assumptions:
            lines.append("Assumptions:")
            lines.extend(f"  - {a}" for a in self.assumptions)
        if self.symbols:
            lines.append("Symbols:")
            lines.extend(f"  {k} = {v}" for k, v in self.symbols.items())
        return "\n".join(lines)


class ContextManager:
    """Builds and tracks :class:`ProblemContext` for a session."""

    def __init__(self) -> None:
        self._stack: list[ProblemContext] = []

    @property
    def current(self) -> ProblemContext | None:
        return self._stack[-1] if self._stack else None

    def push(self, statement: str, domain: str = "unknown", **kw: Any) -> ProblemContext:
        ctx = ProblemContext(statement=statement, domain=domain, **kw)
        self._stack.append(ctx)
        return ctx

    def pop(self) -> ProblemContext | None:
        return self._stack.pop() if self._stack else None
