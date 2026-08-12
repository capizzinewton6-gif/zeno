"""Track analytical steps, numerical validations, and writing tasks."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    description: str = ""
    status: str = "todo"  # todo | in_progress | done
    created: str = ""
    completed: Optional[str] = None


class TaskManager:
    """A lightweight in-memory task tracker for physics projects."""

    def __init__(self):
        self._tasks: list[Task] = []

    def add(self, title: str, description: str = "") -> dict:
        t = Task(title=title, description=description, created=time.strftime("%Y-%m-%d %H:%M"))
        self._tasks.append(t)
        return t.__dict__

    def list(self, status: str | None = None) -> list[dict]:
        if status:
            return [t.__dict__ for t in self._tasks if t.status == status]
        return [t.__dict__ for t in self._tasks]

    def complete(self, title: str) -> bool:
        for t in self._tasks:
            if t.title == title:
                t.status = "done"
                t.completed = time.strftime("%Y-%m-%d %H:%M")
                return True
        return False

    def summary(self) -> dict:
        return {
            "total": len(self._tasks),
            "done": sum(1 for t in self._tasks if t.status == "done"),
            "todo": sum(1 for t in self._tasks if t.status == "todo"),
            "in_progress": sum(1 for t in self._tasks if t.status == "in_progress"),
        }
