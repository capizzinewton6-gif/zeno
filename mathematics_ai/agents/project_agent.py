"""Project agent: manages research and proof projects."""

from __future__ import annotations

from typing import Any

from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.memory import research_notes, proven_theorems


class ProjectAgent(BaseAgent):
    """Tracks research projects, tasks, and proven theorems."""

    name = "project_agent"

    def create_project(self, title: str, description: str = "") -> AgentResult:
        record = research_notes.add({"title": title, "description": description, "tasks": [], "status": "active"})
        return self.result({"project_id": record["id"], "title": title}, steps=[{"action": "create"}])

    def add_task(self, project_id: str, task: str) -> AgentResult:
        for project in research_notes.all():
            if project["id"] == project_id:
                project.setdefault("tasks", []).append({"task": task, "done": False})
                research_notes._save()
                return self.result({"project_id": project_id, "task": task}, steps=[{"action": "add_task"}])
        return self.fail(f"project {project_id} not found")

    def complete_task(self, project_id: str, task_index: int) -> AgentResult:
        for project in research_notes.all():
            if project["id"] == project_id and task_index < len(project.get("tasks", [])):
                project["tasks"][task_index]["done"] = True
                research_notes._save()
                return self.result({"project_id": project_id, "task_index": task_index, "done": True})
        return self.fail("task not found")

    def record_theorem(self, name: str, statement: str, proof: str = "") -> AgentResult:
        record = proven_theorems.add({"name": name, "statement": statement, "proof": proof, "status": "proven"})
        return self.result({"theorem_id": record["id"], "name": name}, steps=[{"action": "record_theorem"}])

    def list_projects(self) -> AgentResult:
        return self.result([
            {"id": p["id"], "title": p.get("title") or p.get("name"), "status": p.get("status")}
            for p in research_notes.all()
        ])

    def list_theorems(self) -> AgentResult:
        return self.result([{"id": t["id"], "name": t.get("name"), "statement": t.get("statement")} for t in proven_theorems.all()])
