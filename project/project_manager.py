"""Coordinates developer sessions, task lists, and goals."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from config import load_json, memory_file, save_json
from project.task_manager import Task, TaskManager


@dataclass
class Session:
    id: str
    goal: str
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "active"
    tasks: list[Task] = field(default_factory=list)


@dataclass
class ProjectState:
    name: str
    goal: str
    stack: list[str] = field(default_factory=list)
    sessions: list[Session] = field(default_factory=list)
    created_at: str = ""


class ProjectManager:
    """Coordinates developer sessions and project goals."""

    def __init__(self, task_manager: TaskManager | None = None) -> None:
        self.tasks = task_manager or TaskManager()
        self._state = self._load()

    def create_project(self, name: str, goal: str, stack: list[str] | None = None) -> ProjectState:
        self._state = ProjectState(
            name=name, goal=goal, stack=stack or [],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._save()
        return self._state

    def start_session(self, goal: str) -> Session:
        import uuid
        session = Session(id=str(uuid.uuid4()), goal=goal)
        self._state.sessions.append(session)
        self._save()
        return session

    def end_session(self, session_id: str) -> bool:
        for s in self._state.sessions:
            if s.id == session_id:
                s.status = "completed"
                self._save()
                return True
        return False

    def state(self) -> ProjectState:
        return self._state

    def summary(self) -> dict[str, Any]:
        active = sum(1 for s in self._state.sessions if s.status == "active")
        return {
            "project": self._state.name,
            "goal": self._state.goal,
            "stack": self._state.stack,
            "sessions_total": len(self._state.sessions),
            "sessions_active": active,
            "tasks": self.tasks.progress(),
        }

    def _load(self) -> ProjectState:
        data = load_json(memory_file("project_context.json"))
        sessions = [Session(**s) for s in data.get("sessions", [])]
        return ProjectState(
            name=data.get("name", ""),
            goal=data.get("project_goal", ""),
            stack=data.get("technology_stack", []),
            sessions=sessions,
            created_at=data.get("created_at", ""),
        )

    def _save(self) -> None:
        data = {
            "name": self._state.name,
            "project_goal": self._state.goal,
            "technology_stack": self._state.stack,
            "created_at": self._state.created_at,
            "sessions": [s.__dict__ for s in self._state.sessions],
            "version": "1.0.0",
        }
        save_json(memory_file("project_context.json"), data)
