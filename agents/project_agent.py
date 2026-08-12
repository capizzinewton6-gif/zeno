"""Project agent: manages engineering projects end-to-end."""

from __future__ import annotations

from ai_core.ai_engine import AIEngine
from project import ProjectManager, TaskManager, VersionManager, Documentation, ReportGenerator


class ProjectAgent:
    def __init__(self, engine: AIEngine | None = None, memory_dir: str = "memory"):
        self.engine = engine or AIEngine()
        self.projects = ProjectManager(memory_dir)
        self.tasks = TaskManager()
        self.versions = VersionManager()
        self.docs = Documentation(self.engine.primary)
        self.reports = ReportGenerator(self.engine.primary)

    def create(self, name: str, description: str, discipline: str = "") -> dict:
        project = self.projects.create(name, description, discipline)
        plan = self.engine.reason(
            f"Decompose this project into a task list: {description}",
            system="You are a project planner.")
        for line in [l for l in plan.split("\n") if l.strip()][:15]:
            self.tasks.add(line.strip("-*0123456789. ").strip())
        project["plan"] = plan
        return project

    def status(self, project_id: str) -> dict:
        project = self.projects.get(project_id)
        return {"project": project, "tasks": self.tasks.summary()}

    def generate_report(self, project_id: str) -> str:
        project = self.projects.get(project_id)
        if not project:
            return "Project not found"
        return self.reports.generate(project["name"])
