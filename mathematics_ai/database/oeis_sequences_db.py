"""Local offline cache of integer sequences (OEIS subset)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).resolve().parent / "oeis_sequences.json"

_DEFAULT_SEQUENCES: list[dict[str, Any]] = [
    {"oeis_id": "A000045", "name": "Fibonacci", "terms": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]},
    {"oeis_id": "A000040", "name": "Primes", "terms": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    {"oeis_id": "A000079", "name": "Powers of 2", "terms": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]},
    {"oeis_id": "A000010", "name": "Euler totient", "terms": [1, 1, 2, 2, 4, 2, 6, 4, 6, 4]},
    {"oeis_id": "A000108", "name": "Catalan", "terms": [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]},
    {"oeis_id": "A000142", "name": "Factorials", "terms": [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]},
    {"oeis_id": "A000217", "name": "Triangular numbers", "terms": [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]},
    {"oeis_id": "A000292", "name": "Tetrahedral numbers", "terms": [1, 4, 10, 20, 35, 56, 84, 120, 165, 220]},
    {"oeis_id": "A001006", "name": "Motzkin", "terms": [1, 1, 2, 4, 9, 21, 51, 127, 323, 835]},
    {"oeis_id": "A001220", "name": "Wieferich primes", "terms": [109, 3511]},
    {"oeis_id": "A001113", "name": "Digits of e", "terms": [2, 7, 1, 8, 2, 8, 1, 8, 2, 8]},
    {"oeis_id": "A000796", "name": "Digits of pi", "terms": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]},
]


def _load() -> list[dict[str, Any]]:
    if not DB_FILE.exists():
        _save(_DEFAULT_SEQUENCES)
    with open(DB_FILE) as f:
        return json.load(f)


def _save(data: list[dict[str, Any]]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def search_by_prefix(prefix: list[int]) -> list[dict[str, Any]]:
    data = _load()
    matches = []
    for seq in data:
        terms = seq["terms"]
        if terms[:len(prefix)] == prefix:
            matches.append(seq)
    return matches


def get_by_id(oeis_id: str) -> dict[str, Any] | None:
    for s in _load():
        if s["oeis_id"] == oeis_id:
            return s
    return None


def list_all() -> list[dict[str, Any]]:
    return _load()


def add(seq: dict[str, Any]) -> None:
    data = _load()
    data.append(seq)
    _save(data)


__all__ = ["search_by_prefix", "get_by_id", "list_all", "add", "DB_FILE"]
