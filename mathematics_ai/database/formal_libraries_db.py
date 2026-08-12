"""Indexed Lean/Coq/Isabelle formal proof modules (Mathlib subset)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).resolve().parent / "formal_libraries.json"

_DEFAULT_MODULES: list[dict[str, str]] = [
    {"name": "Mathlib.Data.Nat.Basic", "system": "Lean 4", "description": "Basic natural number properties"},
    {"name": "Mathlib.Algebra.Group.Basic", "system": "Lean 4", "description": "Group axioms and basic lemmas"},
    {"name": "Mathlib.Algebra.Ring.Basic", "system": "Lean 4", "description": "Ring axioms"},
    {"name": "Mathlib.Algebra.Field.Basic", "system": "Lean 4", "description": "Field axioms"},
    {"name": "Mathlib.Topology.Basic", "system": "Lean 4", "description": "Topological spaces"},
    {"name": "Mathlib.Analysis.Calculus.Deriv", "system": "Lean 4", "description": "Derivatives"},
    {"name": "Mathlib.Data.Complex.Basic", "system": "Lean 4", "description": "Complex numbers"},
    {"name": "Coq.Numbers.Natural.Abstract.NParity", "system": "Coq", "description": "Parity of natural numbers"},
    {"name": "Coq.Lists.ListSet", "system": "Coq", "description": "Finite sets as lists"},
    {"name": "Isabelle.HOL.Main", "system": "Isabelle/HOL", "description": "Main HOL theory"},
]


def _load() -> list[dict[str, str]]:
    if not DB_FILE.exists():
        _save(_DEFAULT_MODULES)
    with open(DB_FILE) as f:
        return json.load(f)


def _save(data: list[dict[str, str]]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def search(query: str) -> list[dict[str, str]]:
    data = _load()
    q = query.lower()
    return [m for m in data if q in m["name"].lower() or q in m["description"].lower() or q in m["system"].lower()]


def by_system(system: str) -> list[dict[str, str]]:
    return [m for m in _load() if m["system"].lower() == system.lower()]


def list_all() -> list[dict[str, str]]:
    return _load()


__all__ = ["search", "by_system", "list_all", "DB_FILE"]
