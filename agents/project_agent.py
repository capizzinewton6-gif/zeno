"""Manages physics research, simulations, and LaTeX paper workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from project.research_manager import ResearchManager
from project.task_manager import TaskManager
from project.documentation import Documentation
from project.paper_generator import PaperGenerator


class ProjectAgent:
    """Coordinates research-project lifecycle: research, tasks, docs, papers."""

    def __init__(self):
        self.research = ResearchManager()
        self.tasks = TaskManager()
        self.docs = Documentation()
        self.papers = PaperGenerator()

    def new_project(self, title: str) -> dict:
        return self.research.create(title)

    def add_task(self, title: str, description: str = "") -> dict:
        return self.tasks.add(title, description)

    def generate_report(self, title: str, body: str) -> str:
        return self.docs.generate(title, body)

    def generate_paper(self, title: str, abstract: str, sections: dict[str, str]) -> str:
        return self.papers.generate(title, abstract, sections)
