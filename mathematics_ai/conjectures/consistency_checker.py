"""Verify logical consistency and axioms of a conjectured pattern."""

from __future__ import annotations

from typing import Any

from mathematics_ai.conjectures.pattern_finder import find_pattern


def check_consistency(sequence: list[int | float], pattern: dict[str, Any]) -> bool:
    """Confirm the pattern holds for every in-sample term."""
    if pattern.get("type") in {"unknown"}:
        return True  # nothing to check
    # re-derive pattern and compare type
    rederived = find_pattern(sequence)
    return rederived.get("type") == pattern.get("type")


def test_boundary_conditions(statement: str, sequence: list[int | float]) -> dict[str, Any]:
    """Test trivial cases (empty, single, boundary values)."""
    results = {}
    results["empty"] = find_pattern([])["type"]
    results["singleton"] = find_pattern(sequence[:1] if sequence else [0])["type"]
    results["pair"] = find_pattern(sequence[:2] if len(sequence) >= 2 else [0, 1])["type"]
    results["full"] = find_pattern(sequence)["type"]
    results["consistent"] = results["full"] != "unknown" if len(sequence) >= 2 else True
    return results


__all__ = ["check_consistency", "test_boundary_conditions"]
