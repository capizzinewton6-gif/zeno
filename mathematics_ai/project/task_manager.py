"""Track lemmas, proofs and computation tasks."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    title: str
    kind: str = "task"  # "lemma" | "proof" | "computation" | "task"
    status: str = "todo"  # "todo" | "in_progress" | "done" | "blocked"
    notes: str = ""
    created: float = field(default_factory=time.time)
    completed: float | None = None


class TaskManager:
    """Manages a list of research/proof tasks."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(self, title: str, kind: str = "task") -> Task:
        t = Task(title=title, kind=kind)
        self._tasks.append(t)
        return t

    def complete(self, index: int) -> None:
        if 0 <= index < len(self._tasks):
            self._tasks[index].status = "done"
            self._tasks[index].completed = time.time()

    def block(self, index: int, reason: str = "") -> None:
        if 0 <= index < len(self._tasks):
            self._tasks[index].status = "blocked"
            self._tasks[index].notes = reason

    def list_tasks(self) -> list[Task]:
        return list(self._tasks)

    def by_status(self, status: str) -> list[Task]:
        return [t for t in self._tasks if t.status == status]

    def to_dict(self) -> list[dict[str, Any]]:
        return [t.__dict__ for t in self._tasks]

    def summary(self) -> dict[str, int]:
        statuses = [t.status for t in self._tasks]
        return {
            "total": len(self._tasks),
            "todo": statuses.count("todo"),
            "in_progress": statuses.count("in_progress"),
            "done": statuses.count("done"),
            "blocked": statuses.count("blocked"),
        }


__all__ = ["Task", "TaskManager"]
