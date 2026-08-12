"""Knowledge graph of software patterns, libraries, and frameworks.

A lightweight in-memory graph of concepts (patterns, libraries, frameworks,
languages) and their relationships, used to ground agent recommendations.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Concept:
    name: str
    kind: str  # pattern, library, framework, language, principle
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class KnowledgeEdge:
    src: str
    dst: str
    relation: str  # "uses", "implements", "alternative-to", "depends-on"


class KnowledgeEngine:
    """In-memory knowledge graph with seed data."""

    def __init__(self) -> None:
        self._concepts: dict[str, Concept] = {}
        self._edges: list[KnowledgeEdge] = []
        self._adj: dict[str, list[tuple[str, str]]] = defaultdict(list)
        self._seed()

    def add(self, concept: Concept) -> None:
        self._concepts[concept.name] = concept

    def relate(self, src: str, dst: str, relation: str) -> None:
        self._edges.append(KnowledgeEdge(src, dst, relation))
        self._adj[src].append((dst, relation))

    def get(self, name: str) -> Concept | None:
        return self._concepts.get(name)

    def neighbors(self, name: str, relation: str | None = None) -> list[str]:
        out = []
        for dst, rel in self._adj.get(name, []):
            if relation is None or rel == relation:
                out.append(dst)
        return out

    def search(self, tag: str) -> list[Concept]:
        return [c for c in self._concepts.values() if tag in c.tags or tag in c.kind]

    def recommend_for(self, language: str, goal: str) -> list[str]:
        """Suggest patterns/libraries for a language+goal pairing."""
        recs: list[str] = []
        for c in self._concepts.values():
            if language.lower() in c.tags and any(g in c.description.lower() for g in goal.lower().split()):
                recs.append(f"{c.name} ({c.kind}): {c.description}")
        return recs[:10]

    # -- seed data -----------------------------------------------------------
    def _seed(self) -> None:
        self.add(Concept("MVC", "pattern", "Model-View-Controller separation", ["architecture", "python", "web"]))
        self.add(Concept("Repository Pattern", "pattern", "Abstract data access behind a repository interface", ["data", "architecture"]))
        self.add(Concept("Factory", "pattern", "Encapsulate object creation", ["creational"]))
        self.add(Concept("Observer", "pattern", "Pub/sub event propagation", ["behavioral"]))
        self.add(Concept("FastAPI", "framework", "Modern async Python web framework", ["python", "web", "api"]))
        self.add(Concept("Flask", "framework", "Lightweight WSGI Python web framework", ["python", "web"]))
        self.add(Concept("React", "framework", "Component-based UI library", ["javascript", "typescript", "web"]))
        self.add(Concept("Vue", "framework", "Progressive JS UI framework", ["javascript", "typescript", "web"]))
        self.add(Concept("Express", "framework", "Node.js web server framework", ["javascript", "node", "web"]))
        self.add(Concept("Actix", "framework", "Rust actor web framework", ["rust", "web"]))
        self.add(Concept("Gin", "framework", "Go HTTP web framework", ["go", "web"]))
        self.add(Concept("pytest", "library", "Python testing framework", ["python", "testing"]))
        self.add(Concept("SQLAlchemy", "library", "Python SQL toolkit and ORM", ["python", "database"]))
        self.add(Concept("Prisma", "library", "TypeScript-first ORM", ["typescript", "database"]))
        self.add(Concept("Docker", "tool", "Container packaging and runtime", ["devops", "deployment"]))
        self.add(Concept("Tree-sitter", "library", "Incremental parsing library", ["parsing", "ast"]))

        self.relate("FastAPI", "Flask", "alternative-to")
        self.relate("React", "Vue", "alternative-to")
        self.relate("FastAPI", "SQLAlchemy", "uses")
        self.relate("Prisma", "Express", "uses")
        self.relate("MVC", "FastAPI", "implements")
        self.relate("Repository Pattern", "SQLAlchemy", "implements")
        self.relate("pytest", "Repository Pattern", "uses")
