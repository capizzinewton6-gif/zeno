"""Safety layer: recursion-depth, resource bounds and unprovability checks."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator

from mathematics_ai.config import get_config


class SafetyError(Exception):
    """Raised when a computation exceeds configured safety bounds."""


class SafetyLayer:
    """Enforces resource bounds for autonomous computations."""

    def __init__(self) -> None:
        self.config = get_config()
        self._depth = 0

    @property
    def max_depth(self) -> int:
        return self.config.max_recursion_depth

    @property
    def max_seconds(self) -> float:
        return self.config.max_computation_seconds

    @contextmanager
    def recursion(self) -> Iterator[None]:
        self._depth += 1
        if self._depth > self.max_depth:
            self._depth -= 1
            raise SafetyError(f"recursion depth {self.max_depth} exceeded")
        try:
            yield
        finally:
            self._depth -= 1

    @contextmanager
    def time_bound(self, seconds: float | None = None) -> Iterator[None]:
        limit = seconds if seconds is not None else self.max_seconds
        start = time.monotonic()
        try:
            yield
        finally:
            elapsed = time.monotonic() - start
            if elapsed > limit:
                raise SafetyError(f"computation exceeded {limit}s (took {elapsed:.2f}s)")

    def check_provable(self, statement: str) -> dict[str, str]:
        """Heuristic flagging of statements that may be undecidable/unprovable.

        Recognises a few well-known families by keyword so the orchestrator can
        decline or mark low-confidence rather than spinning forever.
        """
        lowered = statement.lower()
        known_hard = {
            "continuum hypothesis": "independent of ZFC (undecidable in ZFC)",
            "axiom of choice": "independent of ZF",
            "halting problem": "undecidable (Turing)",
            "riemann hypothesis": "open Millennium problem",
            "p = np": "open Millennium problem",
            "p vs np": "open Millennium problem",
            "goldbach": "open conjecture",
            "twin prime": "open conjecture (partially resolved bounds)",
            "collatz": "open conjecture",
        }
        for key, note in known_hard.items():
            if key in lowered:
                return {"provable": "unknown", "note": note}
        return {"provable": "likely", "note": "no known obstruction detected"}
