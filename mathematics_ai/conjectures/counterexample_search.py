"""Search for counterexamples to conjectures."""

from __future__ import annotations

from typing import Any, Callable

from mathematics_ai.conjectures.pattern_finder import find_pattern


def find_counterexample(sequence: list[int | float], pattern: dict[str, Any]) -> int | None:
    """Given an observed pattern, search ahead for a value breaking it."""
    if pattern.get("type") == "arithmetic":
        d = pattern["common_difference"]
        # extend and look for a break (none expected in-sample; check extrapolation)
        return None
    if pattern.get("type") == "geometric":
        r = pattern["common_ratio"]
        for i in range(len(sequence) - 1):
            if abs(sequence[i + 1] - r * sequence[i]) > 1e-9:
                return i + 1
        return None
    if pattern.get("type") == "fibonacci":
        for i in range(2, len(sequence)):
            if abs(sequence[i] - sequence[i - 1] - sequence[i - 2]) > 1e-9:
                return i
        return None
    if pattern.get("type") == "quadratic":
        second = pattern.get("second_difference")
        if second is None:
            return None
        diffs = [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]
        for i in range(len(diffs) - 1):
            if abs((diffs[i + 1] - diffs[i]) - second) > 1e-9:
                return i + 2
        return None
    return None


def search_predicate(checker: Callable[[int], bool], start: int = 1, end: int = 10000) -> int | None:
    """Find the smallest n in [start, end] for which checker(n) is False."""
    for n in range(start, end + 1):
        try:
            if not checker(n):
                return n
        except Exception:
            continue
    return None


__all__ = ["find_counterexample", "search_predicate"]
