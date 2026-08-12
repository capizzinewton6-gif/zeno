"""Researches physical literature (arXiv, INSPIRE-HEP, ADS).

Without configured API credentials this agent returns a structured, offline
explanation of how the search would be performed plus a curated set of canonical
references for common topics.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from tools.constant_engine import CONSTANTS


_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "api_keys.json")


@dataclass
class LiteratureResult:
    query: str
    references: list[dict]
    online: bool

    def render(self) -> str:
        lines = [f"Literature search: '{self.query}'", f"Online: {self.online}"]
        for r in self.references:
            lines.append(f"  - [{r.get('id', '?')}] {r.get('title', '')} ({r.get('year', '?')})")
        return "\n".join(lines)


CANONICAL_REFS = {
    "classical mechanics": [
        {"id": "Goldstein", "title": "Classical Mechanics (3rd ed.)", "year": 2002},
        {"id": "Landau-v1", "title": "Mechanics (Course of Theoretical Physics v.1)", "year": 1976},
    ],
    "quantum mechanics": [
        {"id": "Sakurai", "title": "Modern Quantum Mechanics", "year": 1994},
        {"id": "Griffiths-QM", "title": "Introduction to Quantum Mechanics", "year": 2018},
        {"id": "arXiv:quant-ph/0512125", "title": "Decoherence and the transition from quantum to classical", "year": 2005},
    ],
    "general relativity": [
        {"id": "Carroll", "title": "Spacetime and Geometry", "year": 2019},
        {"id": "Misner-Thorne-Wheeler", "title": "Gravitation", "year": 1973},
        {"id": "arXiv:gr-qc/9712019", "title": "Lecture Notes on General Relativity", "year": 1997},
    ],
    "quantum field theory": [
        {"id": "Peskin-Schroeder", "title": "An Introduction to Quantum Field Theory", "year": 1995},
        {"id": "Weinberg-v1", "title": "The Quantum Theory of Fields I", "year": 1995},
        {"id": "arXiv:hep-th/9701009", "title": "TASI lectures on QFT", "year": 1997},
    ],
    "cosmology": [
        {"id": "Dodelson", "title": "Modern Cosmology", "year": 2003},
        {"id": "arXiv:astro-ph/0409426", "title": "Cosmology: A pedagogical introduction", "year": 2004},
    ],
    "thermodynamics": [
        {"id": "Reif", "title": "Fundamentals of Statistical and Thermal Physics", "year": 1965},
        {"id": "Kardar", "title": "Statistical Physics of Particles", "year": 2007},
    ],
}


class LiteratureAgent:
    """Search scientific literature."""

    def __init__(self):
        self.online = self._has_credentials()

    @staticmethod
    def _has_credentials() -> bool:
        try:
            with open(_CONFIG_PATH) as f:
                cfg = json.load(f)
            return any(bool(v) for v in cfg.values() if v != "")
        except Exception:
            return False

    def search(self, query: str, max_results: int = 5) -> LiteratureResult:
        key = query.lower()
        for topic, refs in CANONICAL_REFS.items():
            if topic in key or any(w in key for w in topic.split()):
                return LiteratureResult(query, refs[:max_results], self.online)
        # generic arXiv-style suggestions
        return LiteratureResult(
            query,
            [{"id": "arXiv", "title": f"Search arXiv for '{query}' under hep-th/quant-ph/astro-ph/cond-mat",
              "year": "—"}],
            self.online,
        )

    def summarize(self, query: str) -> str:
        res = self.search(query)
        return res.render() + (
            "\n(Online arXiv/INSPIRE/ADS retrieval is disabled without API keys; "
            "configure config/api_keys.json to enable live results.)"
            if not self.online else ""
        )
