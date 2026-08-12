"""Manages language specifications and API reference links."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Reference:
    name: str
    url: str
    category: str  # language, framework, library, standard
    version: str = ""


class ReferenceManager:
    """Catalog of authoritative language/API references."""

    REFERENCES: list[Reference] = [
        Reference("Python Docs", "https://docs.python.org/3/", "language", "3.13"),
        Reference("TypeScript Handbook", "https://www.typescriptlang.org/docs/", "language"),
        Reference("Rust Book", "https://doc.rust-lang.org/book/", "language"),
        Reference("Go Docs", "https://go.dev/doc/", "language"),
        Reference("C++ Reference", "https://en.cppreference.com/", "language"),
        Reference("Java SE Docs", "https://docs.oracle.com/en/java/javase/21/", "language", "21"),
        Reference("MDN Web Docs", "https://developer.mozilla.org/", "framework"),
        Reference("FastAPI", "https://fastapi.tiangolo.com/", "framework"),
        Reference("Django", "https://docs.djangoproject.com/", "framework"),
        Reference("React", "https://react.dev/", "framework"),
        Reference("Vue", "https://vuejs.org/guide/", "framework"),
        Reference("SQLAlchemy", "https://docs.sqlalchemy.org/", "library"),
        Reference("pytest", "https://docs.pytest.org/", "library"),
        Reference("OWASP Top 10", "https://owasp.org/www-project-top-ten/", "standard"),
        Reference("PEP 8", "https://peps.python.org/pep-0008/", "standard"),
        Reference("tree-sitter", "https://tree-sitter.github.io/tree-sitter/", "library"),
        Reference("Gemini API", "https://ai.google.dev/gemini-api/docs", "library"),
    ]

    def __init__(self) -> None:
        self._refs = list(self.REFERENCES)

    def find(self, query: str) -> list[Reference]:
        q = query.lower()
        return [r for r in self._refs
                if q in r.name.lower() or q in r.category.lower()]

    def by_category(self, category: str) -> list[Reference]:
        return [r for r in self._refs if r.category == category]

    def add(self, ref: Reference) -> None:
        self._refs.append(ref)

    def all(self) -> list[Reference]:
        return list(self._refs)
