"""Search the Online Encyclopedia of Integer Sequences (OEIS).

When network access is available, queries the OEIS REST API. Otherwise falls
back to a small built-in lookup of famous sequences so the agent still returns
useful results offline.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

OEIS_API = "https://oeis.org/search"

# A tiny offline cache of well-known sequences (first terms).
KNOWN_SEQUENCES: dict[str, dict[str, Any]] = {
    "A000045": {"name": "Fibonacci", "terms": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]},
    "A000040": {"name": "Primes", "terms": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]},
    "A000079": {"name": "Powers of 2", "terms": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]},
    "A000010": {"name": "Euler totient", "terms": [1, 1, 2, 2, 4, 2, 6, 4, 6, 4]},
    "A000142": {"name": "Factorials", "terms": [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]},
    "A000108": {"name": "Catalan", "terms": [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]},
    "A000217": {"name": "Triangular", "terms": [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]},
    "A000041": {"name": "Partition numbers", "terms": [1, 1, 2, 3, 5, 7, 11, 15, 22, 30]},
    "A001220": {"name": "Wieferich primes", "terms": [109, 3511]},
    "A001006": {"name": "Motzkin", "terms": [1, 1, 2, 4, 9, 21, 51, 127, 323, 835]},
}


def oeis_lookup(sequence: list[int]) -> dict[str, Any]:
    """Look up a sequence by its first terms. Tries the API, falls back offline."""
    try:
        return _oeis_api_lookup(sequence)
    except Exception:
        return oeis_search_offline(sequence)


def _oeis_api_lookup(sequence: list[int]) -> dict[str, Any]:
    query = ",".join(str(s) for s in sequence[:10])
    url = OEIS_API + "?fmt=json&q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mathematics-AI/0.1"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for r in data.get("results", []) or []:
        results.append({
            "oeis_id": r.get("number", ""),
            "name": r.get("name", ""),
            "terms": r.get("data", "").split(",")[:10],
        })
    return {"source": "oeis_api", "matches": results}


def oeis_search_offline(sequence: list[int]) -> dict[str, Any]:
    """Match a sequence prefix against the built-in known-sequence cache."""
    matches = []
    for a_id, info in KNOWN_SEQUENCES.items():
        if info["terms"][:len(sequence)] == sequence:
            matches.append({"oeis_id": a_id, "name": info["name"], "terms": info["terms"]})
    return {"source": "offline_cache", "matches": matches}


__all__ = ["oeis_lookup", "oeis_search_offline", "KNOWN_SEQUENCES"]
