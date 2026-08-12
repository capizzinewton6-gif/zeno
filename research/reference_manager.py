"""Reference manager for citations."""

from __future__ import annotations

import json
import os
from typing import List


class ReferenceManager:
    def __init__(self):
        self.references: List[dict] = []

    def add(self, key: str, authors: str, title: str, year: int,
            venue: str = "", doi: str = "", url: str = ""):
        self.references.append({
            "key": key, "authors": authors, "title": title,
            "year": year, "venue": venue, "doi": doi, "url": url,
        })

    def all(self) -> List[dict]:
        return list(self.references)

    def by_key(self, key: str) -> dict | None:
        for r in self.references:
            if r["key"] == key:
                return r
        return None

    def ieee(self) -> str:
        lines = []
        for i, r in enumerate(self.references, 1):
            line = f'[{i}] {r["authors"]}, "{r["title"]}"'
            if r["venue"]:
                line += f', {r["venue"]}'
            line += f', {r["year"]}.'
            if r["doi"]:
                line += f' doi: {r["doi"]}.'
            lines.append(line)
        return "\n".join(lines)

    def bibtex(self) -> str:
        lines = []
        for r in self.references:
            entry_type = "article" if r["venue"] else "misc"
            lines.append(f'@{entry_type}{{{r["key"]},')
            lines.append(f'  author = {{{r["authors"]}}},')
            lines.append(f'  title = {{{r["title"]}}},')
            if r["venue"]:
                lines.append(f'  journal = {{{r["venue"]}}},')
            lines.append(f'  year = {{{r["year"]}}},')
            if r["doi"]:
                lines.append(f'  doi = {{{r["doi"]}}},')
            lines.append('}')
        return "\n".join(lines)

    def save(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.references, f, indent=2)
        return path

    def load(self, path: str):
        with open(path, encoding="utf-8") as f:
            self.references = json.load(f)
