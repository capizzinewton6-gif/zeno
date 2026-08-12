"""Project agent — manages synthesis and materials research projects."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import ResearchManager, TaskManager, NotebookManager, Documentation, PaperGenerator
from src.gemini_25_flash_engine import reason as gemini25_reason


class ProjectAgent:
    """Manage research projects, tasks, notebooks, and documentation."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.research = ResearchManager()
        self.tasks = TaskManager()
        self.notebook = NotebookManager()
        self.docs = Documentation()
        self.paper = PaperGenerator(api_key=api_key)

    def handle(self, request):
        task = request.get("task", "")
        params = request.get("params", {}) or {}
        text = task.lower()
        if "project" in text and "create" in text:
            return {"agent": "ProjectAgent", "capability": "create_project",
                    "result": self.research.create_project(params.get("name", "New Project"),
                                                           params.get("target"),
                                                           params.get("description", ""))}
        if "task" in text:
            return {"agent": "ProjectAgent", "capability": "add_task",
                    "result": self.tasks.add_task(params.get("title", task),
                                                  params.get("category", "synthesis"))}
        if "notebook" in text or "eln" in text:
            return {"agent": "ProjectAgent", "capability": "notebook",
                    "result": self.notebook.add_entry(params.get("title", "Entry"),
                                                      params.get("body", task))}
        if "manuscript" in text or "paper" in text:
            return {"agent": "ProjectAgent", "capability": "paper_generation",
                    "result": self.paper.generate(params.get("title", "Untitled"),
                                                  params.get("authors", ["Author, A."]),
                                                  params.get("abstract", ""),
                                                  params.get("results", ""),
                                                  params.get("experimental", ""))}
        if "characterization" in text or "nmr table" in text:
            return {"agent": "ProjectAgent", "capability": "documentation",
                    "result": self.docs.characterization_summary(params.get("compound", "Unknown"),
                                                                  nmr=params.get("nmr"),
                                                                  hrms=params.get("hrms"))}
        return {"agent": "ProjectAgent", "capability": "overview",
                "result": {"projects": self.research.list_projects(),
                           "tasks": self.tasks.summary()}}
