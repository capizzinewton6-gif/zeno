"""Manage biological research projects."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


class ResearchProject:
    def __init__(self, name: str, objective: str, organism: str = ""):
        self.name = name
        self.objective = objective
        self.organism = organism
        self.created_at = datetime.utcnow().isoformat()
        self.status = "planning"
        self.notes: list[str] = []
        self.experiments: list[dict] = []
        self.tasks: list[dict] = []

    def add_note(self, note: str) -> None:
        self.notes.append({"time": datetime.utcnow().isoformat(), "text": note})

    def add_experiment(self, exp_id: str, description: str) -> None:
        self.experiments.append({"id": exp_id, "description": description,
                                  "status": "planned", "created_at": datetime.utcnow().isoformat()})

    def set_status(self, status: str) -> None:
        self.status = status

    def to_dict(self) -> dict:
        return {"name": self.name, "objective": self.objective,
                "organism": self.organism, "created_at": self.created_at,
                "status": self.status, "notes": self.notes,
                "experiments": self.experiments, "tasks": self.tasks}


class ResearchManager:
    def __init__(self):
        self.projects: dict[str, ResearchProject] = {}

    def create(self, name: str, objective: str, organism: str = "") -> ResearchProject:
        p = ResearchProject(name, objective, organism)
        self.projects[name] = p
        return p

    def get(self, name: str) -> ResearchProject | None:
        return self.projects.get(name)

    def list_projects(self) -> list[str]:
        return list(self.projects.keys())

    def save(self, path: str | Path) -> str:
        Path(path).write_text(json.dumps(
            {n: p.to_dict() for n, p in self.projects.items()},
            indent=2), encoding="utf-8")
        return str(path)
