"""Manage theoretical physics derivations and simulation experiments."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field


_PROJECTS_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "research_notes.json")


@dataclass
class ResearchProject:
    id: str
    title: str
    created: str
    status: str = "active"
    notes: list[str] = field(default_factory=list)
    derivations: list[str] = field(default_factory=list)


class ResearchManager:
    """Track active research projects and derivations."""

    def __init__(self, path: str | None = None):
        self.path = path or _PROJECTS_PATH

    def create(self, title: str) -> dict:
        proj = ResearchProject(id=f"proj-{int(time.time())}", title=title,
                                created=time.strftime("%Y-%m-%d %H:%M"))
        return proj.__dict__

    def list(self) -> list:
        try:
            with open(self.path) as f:
                return json.load(f).get("derivations", [])
        except Exception:
            return []

    def add_derivation(self, derivation: str) -> None:
        try:
            with open(self.path) as f:
                data = json.load(f)
        except Exception:
            data = {"derivations": []}
        data.setdefault("derivations", []).append(derivation)
        data["last_updated"] = time.strftime("%Y-%m-%d %H:%M")
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
