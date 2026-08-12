"""Manage BibTeX and citations."""
from __future__ import annotations

from collections import OrderedDict


class ReferenceManager:
    def __init__(self):
        self.references: OrderedDict[str, dict] = OrderedDict()

    def add(self, key: str, ref_type: str, fields: dict) -> dict:
        entry = {"type": ref_type, **fields}
        self.references[key] = entry
        return entry

    def add_article(self, key: str, authors: str, title: str, journal: str,
                    year: int, volume: str = "", pages: str = "",
                    doi: str = "") -> dict:
        fields = {"author": authors, "title": title, "journal": journal,
                   "year": str(year)}
        if volume:
            fields["volume"] = volume
        if pages:
            fields["pages"] = pages
        if doi:
            fields["doi"] = doi
        return self.add(key, "article", fields)

    def to_bibtex(self) -> str:
        lines = []
        for key, ref in self.references.items():
            lines.append(f"@{ref['type']}{{{key},")
            for k, v in ref.items():
                if k == "type":
                    continue
                lines.append(f"  {k} = {{{v}}},")
            lines.append("}\n")
        return "\n".join(lines)

    def cite(self, key: str) -> str:
        ref = self.references.get(key)
        if not ref:
            return f"[Unknown reference {key}]"
        author = ref.get("author", "").split(",")[0].strip()
        year = ref.get("year", "")
        return f"{author} et al., {year}"

    def search(self, term: str) -> list[str]:
        t = term.lower()
        return [k for k, r in self.references.items()
                if t in r.get("title", "").lower() or t in r.get("author", "").lower()]
