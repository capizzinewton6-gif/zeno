"""Track cloning steps, assays, and sequencing runs."""
from __future__ import annotations

from datetime import datetime


class TaskManager:
    def __init__(self):
        self.tasks: list[dict] = []
        self._next_id = 1

    def add(self, title: str, category: str = "general",
            priority: str = "medium", due: str = "") -> dict:
        task = {"id": self._next_id, "title": title, "category": category,
                "priority": priority, "due": due,
                "status": "todo", "created": datetime.utcnow().isoformat()}
        self.tasks.append(task)
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> dict | None:
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = "done"
                t["completed"] = datetime.utcnow().isoformat()
                return t
        return None

    def by_category(self, category: str) -> list[dict]:
        return [t for t in self.tasks if t["category"] == category]

    def pending(self) -> list[dict]:
        return [t for t in self.tasks if t["status"] != "done"]

    def summary(self) -> dict:
        return {"total": len(self.tasks),
                "pending": len(self.pending()),
                "done": len([t for t in self.tasks if t["status"] == "done"])}

    @staticmethod
    def clone_pipeline_steps(gene: str, vector: str = "pUC19") -> list[dict]:
        return [
            {"title": f"Design primers for {gene}", "category": "cloning"},
            {"title": "PCR amplify insert", "category": "cloning"},
            {"title": "Restriction digest insert and vector", "category": "cloning"},
            {"title": f"Ligate {gene} into {vector}", "category": "cloning"},
            {"title": "Transform competent cells", "category": "cloning"},
            {"title": "Screen colonies by colony PCR", "category": "screening"},
            {"title": "Sanger sequence verify", "category": "verification"},
        ]
