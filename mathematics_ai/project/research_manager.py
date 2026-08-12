"""Manage mathematics research projects."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from mathematics_ai.memory import research_notes
from mathematics_ai.project.task_manager import TaskManager


class ResearchProject:
    """A research project: a goal, tasks, and a notebook reference."""

    def __init__(self, name: str, goal: str, project_id: str | None = None) -> None:
        self.id = project_id or f"{int(time.time() * 1000)}"
        self.name = name
        self.goal = goal
        self.created = time.time()
        self.tasks = TaskManager()
        self.notes: list[str] = []
        self.status = "planning"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "goal": self.goal,
            "created": self.created,
            "status": self.status,
            "notes": self.notes,
            "tasks": self.tasks.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ResearchProject":
        name = data.get("name") or data.get("title", "")
        goal = data.get("goal") or data.get("description", "")
        proj = cls(name, goal, data.get("id"))
        proj.created = data.get("created", data.get("created_at", time.time()))
        proj.status = data.get("status", "planning")
        proj.notes = data.get("notes", [])
        for t in data.get("tasks", []):
            if isinstance(t, dict):
                proj.tasks.add(t.get("title", t.get("task", "")), t.get("kind", "task"))
            else:
                proj.tasks.add(str(t), "task")
        return proj


class ResearchManager:
    """Registry of research projects, persisted to memory."""

    def __init__(self) -> None:
        self._projects: dict[str, ResearchProject] = {}
        self._load()

    def create(self, name: str, goal: str) -> ResearchProject:
        proj = ResearchProject(name, goal)
        self._projects[proj.id] = proj
        # also persist as a flat record in the ListStore
        research_notes.add({"id": proj.id, "name": name, "goal": goal, "record_type": "research_manager"})
        return proj

    def get(self, project_id: str) -> ResearchProject | None:
        return self._projects.get(project_id)

    def list_projects(self) -> list[dict[str, Any]]:
        return [p.to_dict() for p in self._projects.values()]

    def add_note(self, project_id: str, note: str) -> None:
        proj = self.get(project_id)
        if proj:
            proj.notes.append(note)
            self._save()

    def set_status(self, project_id: str, status: str) -> None:
        proj = self.get(project_id)
        if proj:
            proj.status = status
            self._save()

    def _load(self) -> None:
        for p in research_notes.all():
            proj = ResearchProject.from_dict(p)
            self._projects[proj.id] = proj

    def _save(self) -> None:
        # ListStore holds a flat list of project records; rebuild it from scratch
        research_notes._data["projects"] = [p.to_dict() for p in self._projects.values()]
        research_notes._save()


__all__ = ["ResearchProject", "ResearchManager"]
