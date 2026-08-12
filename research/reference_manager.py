"""Reference manager: manage research papers, citations, and algorithm docs."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class Reference:
    key: str
    title: str
    authors: List[str] = field(default_factory=list)
    venue: str = ""
    year: int = 0
    url: str = ""
    notes: str = ""


class ReferenceManager:
    """CRUD over a JSON-backed bibliography."""

    def __init__(self, path: str = "memory/references.json") -> None:
        self.path = path
        self.refs: Dict[str, Reference] = {}
        self.load()

    def add(self, ref: Reference) -> None:
        self.refs[ref.key] = ref
        self.save()

    def remove(self, key: str) -> bool:
        if key in self.refs:
            del self.refs[key]
            self.save()
            return True
        return False

    def list(self) -> List[Reference]:
        return sorted(self.refs.values(), key=lambda r: (r.year, r.title), reverse=True)

    def search(self, text: str) -> List[Reference]:
        t = text.lower()
        return [r for r in self.refs.values()
                if t in r.title.lower() or t in r.notes.lower() or any(t in a.lower() for a in r.authors)]

    def to_bibtex(self, key: str) -> str:
        r = self.refs.get(key)
        if not r:
            return ""
        authors = " and ".join(r.authors)
        return (f"@article{{{r.key},\n  title={{{r.title}}},\n  author={{{authors}}},\n"
                f"  journal={{{r.venue}}},\n  year={{{r.year}}},\n  url={{{r.url}}}\n}}")

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w") as f:
            json.dump({k: asdict(v) for k, v in self.refs.items()}, f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path) as f:
            data = json.load(f)
        for k, v in data.items():
            self.refs[k] = Reference(**v)
