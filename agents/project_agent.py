"""Project agent: manages biology research projects."""
from __future__ import annotations

from ai_core.ai_engine import AIEngine


class ProjectAgent:
    def __init__(self, ai: AIEngine | None = None):
        self.ai = ai or AIEngine()
        from project.research_manager import ResearchManager
        from project.task_manager import TaskManager
        from project.notebook_manager import NotebookManager
        self.research = ResearchManager()
        self.tasks = TaskManager()
        self.notebook = NotebookManager()

    def create_project(self, name: str, objective: str, organism: str = "") -> dict:
        p = self.research.create(name, objective, organism)
        return p.to_dict()

    def list_projects(self) -> list[str]:
        return self.research.list_projects()

    def add_task(self, title: str, category: str = "general",
                 priority: str = "medium") -> dict:
        return self.tasks.add(title, category, priority)

    def add_notebook_entry(self, title: str, body: str,
                           tags: list[str] | None = None) -> dict:
        return self.notebook.add_entry(title, body, tags=tags)

    def generate_report(self, title: str, abstract: str, sections: dict,
                        references: list[str] | None = None) -> str:
        from project.report_generator import ReportGenerator
        return ReportGenerator.research_paper(title, abstract, sections, references)

    def generate_lab_report(self, title: str, authors: list[str], abstract: str,
                            introduction: str, methods: str, results: str,
                            discussion: str, references: list[str] | None = None) -> str:
        from project.report_generator import ReportGenerator
        return ReportGenerator.lab_report(title, authors, abstract, introduction,
                                          methods, results, discussion, references)

    def plan_project(self, goal: str, constraints: str = "") -> list[dict]:
        from ai_core.planning_engine import PlanningEngine
        return PlanningEngine(self.ai).plan_experiment(goal, constraints)
