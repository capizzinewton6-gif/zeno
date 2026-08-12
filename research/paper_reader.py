"""Paper reader: parse CV research papers (CVPR, ICCV, ECCV)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Paper:
    title: str = ""
    authors: List[str] = field(default_factory=list)
    abstract: str = ""
    venue: str = ""
    year: int = 0
    sections: dict = field(default_factory=dict)


class PaperReader:
    """Lightweight parser for plain-text / abstract-form papers."""

    @staticmethod
    def parse_text(text: str) -> Paper:
        paper = Paper()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if lines:
            paper.title = lines[0]
        # Abstract block
        try:
            start = next(i for i, l in enumerate(lines) if l.lower().startswith("abstract"))
            abstract_lines = []
            for l in lines[start + 1:]:
                if re.match(r"^(1\.|introduction|keywords)", l, re.IGNORECASE):
                    break
                abstract_lines.append(l)
            paper.abstract = " ".join(abstract_lines)
        except StopIteration:
            pass
        # Venue/year heuristics
        for venue in ("CVPR", "ICCV", "ECCV", "NeurIPS", "AAAI"):
            for l in lines[:5]:
                if venue in l:
                    paper.venue = venue
                    m = re.search(r"(20\d{2})", l)
                    if m:
                        paper.year = int(m.group(1))
        return paper

    @staticmethod
    def parse_bibtex(bib: str) -> Paper:
        paper = Paper()
        m = re.search(r"title\s*=\s*\{(.+?)\}", bib, re.IGNORECASE | re.DOTALL)
        if m:
            paper.title = m.group(1).strip()
        m = re.search(r"author\s*=\s*\{(.+?)\}", bib, re.IGNORECASE | re.DOTALL)
        if m:
            paper.authors = [a.strip() for a in m.group(1).split(" and ")]
        m = re.search(r"year\s*=\s*\{(\d{4})\}", bib)
        if m:
            paper.year = int(m.group(1))
        m = re.search(r"booktitle\s*=\s*\{(.+?)\}", bib, re.IGNORECASE)
        if m:
            paper.venue = m.group(1).strip()
        return paper
