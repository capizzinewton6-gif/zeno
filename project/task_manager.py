"""Task manager: engineering task breakdown and tracking."""

from __future__ import annotations

import time
from typing import Any, Dict, List


class TaskManager:
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []

    def add(self, title: str, description: str = "", priority: str = "medium",
            dependencies: list[str] | None = None) -> Dict[str, Any]:
        task = {
            "id": f"task_{len(self.tasks) + 1}",
            "title": title, "description": description,
            "priority": priority, "status": "todo",
            "dependencies": dependencies or [],
            "created_at": time.time(),
        }
        self.tasks.append(task)
        return task

    def update_status(self, task_id: str, status: str) -> bool:
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = status
                return True
        return False

    def get(self, task_id: str) -> Dict[str, Any] | None:
        for t in self.tasks:
            if t["id"] == task_id:
                return t
        return None

    def by_status(self, status: str) -> List[Dict[str, Any]]:
        return [t for t in self.tasks if t["status"] == status]

    def ready(self) -> List[Dict[str, Any]]:
        """Tasks whose dependencies are all done."""
        done = {t["id"] for t in self.tasks if t["status"] == "done"}
        return [t for t in self.tasks
                if t["status"] == "todo" and all(d in done for d in t["dependencies"])]

    def all(self) -> List[Dict[str, Any]]:
        return list(self.tasks)

    def summary(self) -> dict:
        return {
            "total": len(self.tasks),
            "todo": len(self.by_status("todo")),
            "in_progress": len(self.by_status("in_progress")),
            "done": len(self.by_status("done")),
        }
