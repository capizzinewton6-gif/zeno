"""Task manager: track dataset annotation, model training, quantization tasks."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Task:
    id: str
    title: str
    kind: str = "generic"  # annotation | training | quantization | evaluation
    status: str = "todo"  # todo | in_progress | done | blocked
    assignee: str = ""
    created_at: str = ""
    notes: str = ""


class TaskManager:
    """Track operational tasks for a vision project."""

    def __init__(self, store_path: str = "memory/tasks.json") -> None:
        self.store_path = store_path
        self.tasks: Dict[str, Task] = {}
        self._counter = 0
        self.load()

    def add(self, title: str, kind: str = "generic", assignee: str = "") -> Task:
        self._counter += 1
        tid = f"task-{self._counter:04d}"
        t = Task(id=tid, title=title, kind=kind, assignee=assignee,
                 created_at=datetime.utcnow().isoformat())
        self.tasks[tid] = t
        self.save()
        return t

    def update_status(self, task_id: str, status: str) -> bool:
        if task_id in self.tasks and status in ("todo", "in_progress", "done", "blocked"):
            self.tasks[task_id].status = status
            self.save()
            return True
        return False

    def list(self, status: Optional[str] = None) -> List[Task]:
        return [t for t in self.tasks.values() if not status or t.status == status]

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.store_path) or ".", exist_ok=True)
        with open(self.store_path, "w") as f:
            json.dump({k: asdict(v) for k, v in self.tasks.items()}, f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.store_path):
            return
        with open(self.store_path) as f:
            data = json.load(f)
        for k, v in data.items():
            self.tasks[k] = Task(**v)
            try:
                self._counter = max(self._counter, int(k.split("-")[1]))
            except (IndexError, ValueError):
                pass
