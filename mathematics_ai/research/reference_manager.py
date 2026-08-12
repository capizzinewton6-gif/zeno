"""Manage BibTeX entries and citation networks.

A lightweight, dependency-free BibTeX manager: parse, add, search, and export
entries, plus a small citation-graph helper to resolve which entries cite
which others (by key references).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

BIBTEX_ENTRY_RE = re.compile(
    r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,(.*?)\n\}",
    re.DOTALL,
)


@dataclass
class BibEntry:
    key: str
    entry_type: str
    fields: dict[str, str] = field(default_factory=dict)

    def to_bibtex(self) -> str:
        lines = [f"@{self.entry_type}{{{self.key},"]
        for k, v in self.fields.items():
            lines.append(f"  {k} = {{{v}}},")
        lines.append("}")
        return "\n".join(lines)


class ReferenceManager:
    """In-memory BibTeX store with citation-network helpers."""

    def __init__(self) -> None:
        self._entries: dict[str, BibEntry] = {}

    # ------------------------------------------------------------------ IO
    def add(self, entry: BibEntry) -> BibEntry:
        self._entries[entry.key] = entry
        return entry

    def parse_bibtex(self, text: str) -> list[BibEntry]:
        """Parse BibTeX source and register all entries."""
        entries: list[BibEntry] = []
        for m in BIBTEX_ENTRY_RE.finditer(text):
            body = m.group(3)
            fields = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}", body, re.DOTALL))
            entry = BibEntry(key=m.group("key"), entry_type=m.group("type"), fields=fields)
            self.add(entry)
            entries.append(entry)
        return entries

    def export_bibtex(self) -> str:
        return "\n\n".join(e.to_bibtex() for e in self._entries.values())

    # ------------------------------------------------------------------ query
    def get(self, key: str) -> BibEntry | None:
        return self._entries.get(key)

    def all(self) -> list[BibEntry]:
        return list(self._entries.values())

    def search(self, query: str) -> list[BibEntry]:
        ql = query.lower()
        return [
            e for e in self._entries.values()
            if ql in e.key.lower()
            or any(ql in v.lower() for v in e.fields.values())
        ]

    # ------------------------------------------------------------------ network
    def citation_graph(self) -> dict[str, list[str]]:
        """Build a graph mapping each entry key to the keys it cites."""
        graph: dict[str, list[str]] = {}
        for e in self._entries.values():
            cites = [k.strip() for k in re.split(r"[,;\s]+", e.fields.get("cites", "")) if k.strip()]
            graph[e.key] = cites
        return graph

    def cited_by(self, key: str) -> list[str]:
        """Return keys that cite ``key``."""
        graph = self.citation_graph()
        return [src for src, targets in graph.items() if key in targets]

    def statistics(self) -> dict[str, Any]:
        graph = self.citation_graph()
        all_keys = set(self._entries)
        all_targets = {t for targets in graph.values() for t in targets}
        return {
            "entries": len(self._entries),
            "edges": sum(len(t) for t in graph.values()),
            "missing_targets": sorted(all_targets - all_keys),
        }


__all__ = ["BibEntry", "ReferenceManager"]
