"""Finite group tables, Galois groups and Lie algebras."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).resolve().parent / "algebraic_structures.json"

_DEFAULT_STRUCTURES: list[dict[str, Any]] = [
    {"name": "Z_2", "type": "group", "order": 2, "abelian": True, "cyclic": True, "multiplication_table": [[0, 1], [1, 0]]},
    {"name": "Z_3", "type": "group", "order": 3, "abelian": True, "cyclic": True, "multiplication_table": [[0, 1, 2], [1, 2, 0], [2, 0, 1]]},
    {"name": "Z_4", "type": "group", "order": 4, "abelian": True, "cyclic": True, "multiplication_table": [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]},
    {"name": "Klein_4", "type": "group", "order": 4, "abelian": True, "cyclic": False, "multiplication_table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]},
    {"name": "S_3", "type": "group", "order": 6, "abelian": False, "cyclic": False, "note": "symmetric group on 3 elements"},
    {"name": "Z_6", "type": "group", "order": 6, "abelian": True, "cyclic": True},
    {"name": "Q_8", "type": "group", "order": 8, "abelian": False, "cyclic": False, "note": "quaternion group"},
    {"name": "D_4", "type": "group", "order": 8, "abelian": False, "cyclic": False, "note": "dihedral group"},
    {"name": "A_4", "type": "group", "order": 12, "abelian": False, "cyclic": False, "note": "alternating group"},
    {"name": "S_4", "type": "group", "order": 24, "abelian": False, "cyclic": False},
    {"name": "Gal(x^2-2)", "type": "galois_group", "polynomial": "x^2-2", "group": "Z_2"},
    {"name": "Gal(x^3-2)", "type": "galois_group", "polynomial": "x^3-2", "group": "S_3"},
    {"name": "su(2)", "type": "lie_algebra", "dimension": 3, "compact": True},
    {"name": "su(3)", "type": "lie_algebra", "dimension": 8, "compact": True},
    {"name": "sl(2,R)", "type": "lie_algebra", "dimension": 3, "compact": False},
]


def _load() -> list[dict[str, Any]]:
    if not DB_FILE.exists():
        _save(_DEFAULT_STRUCTURES)
    with open(DB_FILE) as f:
        return json.load(f)


def _save(data: list[dict[str, Any]]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def search(query: str) -> list[dict[str, Any]]:
    data = _load()
    q = query.lower()
    return [s for s in data if q in s["name"].lower() or s.get("type", "").lower() == q]


def get(name: str) -> dict[str, Any] | None:
    for s in _load():
        if s["name"].lower() == name.lower():
            return s
    return None


def by_type(structure_type: str) -> list[dict[str, Any]]:
    return [s for s in _load() if s.get("type") == structure_type]


def list_all() -> list[dict[str, Any]]:
    return _load()


__all__ = ["search", "get", "by_type", "list_all", "DB_FILE"]
