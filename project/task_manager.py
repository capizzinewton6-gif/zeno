"""Feature task board, bug lists, and development steps."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from config import load_json, memory_file, save_json

STATUSES = ("todo", "in_progress", "done", "blocked")
PRIORITIES = ("low", "medium", "high", "critical")


@dataclass
class Task:
    id: str
    title: str
    status: str = "todo"
    priority: str = "medium"
    assignee: str = ""
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str = ""


@dataclass
class Bug:
    id: str
    title: str
    severity: str = "medium"
    status: str = "open"  # open, fixed, wontfix
    description: str = ""
    file: str = ""


class TaskManager:
    """In-memory + persisted task board."""

    def __init__(self) -> None:
        self._data = load_json(memory_file("project_context.json"))
        self._tasks: list[Task] = [Task(**t) for t in self._data.get("tasks", [])]
        self._bugs: list[Bug] = [Bug(**b) for b in self._data.get("bugs", [])]

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)
        self._save()

    def add_bug(self, bug: Bug) -> None:
        self._bugs.append(bug)
        self._save()

    def update_task(self, task_id: str, status: str) -> bool:
        for t in self._tasks:
            if t.id == task_id:
                t.status = status
                if status == "done":
                    t.completed_at = datetime.now(timezone.utc).isoformat()
                self._save()
                return True
        return False

    def tasks_by_status(self, status: str) -> list[Task]:
        return [t for t in self._tasks if t.status == status]

    def open_bugs(self) -> list[Bug]:
        return [b for b in self._bugs if b.status == "open"]

    def progress(self) -> dict[str, Any]:
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t.status == "done")
        return {
            "total_tasks": total,
            "done": done,
            "open_bugs": len(self.open_bugs()),
            "completion_pct": (done / total * 100) if total else 0.0,
        }

    def board(self) -> dict[str, list[dict[str, Any]]]:
        return {
            status: [t.__dict__ for t in self._tasks if t.status == status]
            for status in STATUSES
        }

    def _save(self) -> None:
        self._data["tasks"] = [t.__dict__ for t in self._tasks]
        self._data["bugs"] = [b.__dict__ for b in self._bugs]
        save_json(memory_file("project_context.json"), self._data)
