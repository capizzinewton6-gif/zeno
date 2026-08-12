"""Manage algebraic, metric and topological spaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import sympy as sp


@dataclass
class Space:
    name: str
    kind: str  # "algebraic" | "metric" | "topological" | "vector"
    elements: list[Any] = field(default_factory=list)
    operations: dict[str, Callable] = field(default_factory=dict)
    metric: Callable[[Any, Any], float] | None = None
    open_sets: list[list[Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class DomainManager:
    """Registry of mathematical spaces."""

    def __init__(self) -> None:
        self._spaces: dict[str, Space] = {}

    def register(self, space: Space) -> None:
        self._spaces[space.name] = space

    def get(self, name: str) -> Space | None:
        return self._spaces.get(name)

    def list_spaces(self) -> list[str]:
        return list(self._spaces.keys())

    def is_group(self, space: Space) -> bool:
        return space.kind == "algebraic" and all(
            op in space.operations for op in ("mul", "inv", "id")
        )

    def is_metric(self, space: Space) -> bool:
        return space.metric is not None

    def distance(self, space_name: str, a: Any, b: Any) -> float | None:
        s = self.get(space_name)
        if s is None or s.metric is None:
            return None
        return s.metric(a, b)


def make_levy_metric() -> Space:
    """The metric d(x, y) = |x - y| / (1 + |x - y|) on R."""
    def levy(x: float, y: float) -> float:
        d = abs(x - y)
        return d / (1 + d)
    return Space(name="R_levy", kind="metric", metric=levy)


def make_discrete_topology(elements: list[Any]) -> Space:
    """Discrete topology: every subset is open."""
    import itertools
    opens = []
    for r in range(len(elements) + 1):
        for combo in itertools.combinations(elements, r):
            opens.append(list(combo))
    return Space(name="discrete", kind="topological", elements=elements, open_sets=opens)


def make_finite_field(p: int) -> Space:
    """The finite field F_p (prime p) with modular arithmetic."""
    if not sp.isprime(p):
        raise ValueError(f"{p} is not prime")
    elements = list(range(p))
    return Space(
        name=f"F_{p}",
        kind="algebraic",
        elements=elements,
        operations={
            "add": lambda a, b: (a + b) % p,
            "mul": lambda a, b: (a * b) % p,
            "inv": lambda a: pow(a, p - 2, p),
            "id": 0,
        },
    )


__all__ = ["Space", "DomainManager", "make_levy_metric", "make_discrete_topology", "make_finite_field"]
