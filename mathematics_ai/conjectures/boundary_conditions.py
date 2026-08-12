"""Test edge cases and trivial cases of conjectured patterns."""

from __future__ import annotations

from typing import Any

from mathematics_ai.conjectures.pattern_finder import find_pattern


def test_edge_cases(sequence: list[int | float]) -> dict[str, Any]:
    """Check the pattern under degenerate prefixes."""
    results = {}
    results["zero_prefix"] = find_pattern([0] + sequence)["type"]
    results["one_prefix"] = find_pattern([1] + sequence)["type"]
    results["negated"] = find_pattern([-s for s in sequence])["type"]
    results["reversed"] = find_pattern(list(reversed(sequence)))["type"]
    return results


def test_trivial_inputs(pattern: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the pattern for trivial inputs."""
    t = pattern.get("type")
    if t == "arithmetic":
        d = pattern.get("common_difference")
        return {"a_0": 0, "a_1": d, "constant_sequence": d == 0}
    if t == "geometric":
        r = pattern.get("common_ratio")
        return {"a_0": 1, "a_1": r, "constant_sequence": r == 1}
    if t == "quadratic":
        return {"quadratic": True}
    return {"type": t}


__all__ = ["test_edge_cases", "test_trivial_inputs"]
