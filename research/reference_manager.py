"""Manage BibTeX keys and physics citation networks."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Reference:
    key: str
    title: str
    authors: list[str] = field(default_factory=list)
    year: int = 0
    cites: list[str] = field(default_factory=list)


class ReferenceManager:
    """BibTeX-style reference store with citation graph."""

    def __init__(self):
        self.refs: dict[str, Reference] = {}
        self.graph: dict[str, list[str]] = defaultdict(list)

    def add(self, ref: Reference) -> None:
        self.refs[ref.key] = ref
        for c in ref.cites:
            self.graph[ref.key].append(c)

    def bibtex(self, key: str) -> str:
        r = self.refs[key]
        authors = " and ".join(r.authors) if r.authors else "Unknown"
        return (f"@article{{{r.key},\n  title = {{{r.title}}},\n"
                f"  author = {{{authors}}},\n  year = {{{r.year}}},\n}}\n")

    def all_bibtex(self) -> str:
        return "\n".join(self.bibtex(k) for k in self.refs)

    def forward_citations(self, key: str) -> list[str]:
        return list(self.graph.get(key, []))

    def backward_citations(self, key: str) -> list[str]:
        return [k for k, v in self.graph.items() if key in v]
