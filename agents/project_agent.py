"""Project agent: manages video analysis projects, exports, and session logs."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from project.research_manager import ResearchManager
from project.report_generator import ReportGenerator
from project.task_manager import TaskManager


class ProjectAgent:
    """Coordinate project metadata, tasks, and report exports for a session."""

    def __init__(self, project_name: str = "default",
                 research: Optional[ResearchManager] = None,
                 tasks: Optional[TaskManager] = None,
                 report: Optional[ReportGenerator] = None) -> None:
        self.project_name = project_name
        self.research = research or ResearchManager()
        self.tasks = tasks or TaskManager()
        self.report = report or ReportGenerator()
        self.session_log: list = []
        self._ensure_project()

    def _ensure_project(self) -> None:
        if self.project_name not in self.research.projects:
            self.research.create(self.project_name, "Auto-created session")

    def log(self, event: str, details: Dict[str, Any]) -> None:
        self.session_log.append({"ts": datetime.utcnow().isoformat(),
                                 "event": event, "details": details})

    def export_report(self, path: str) -> str:
        out = self.report.save(path)
        self.log("export_report", {"path": out})
        return out

    def export_session(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        payload = {"project": self.project_name,
                   "session_log": self.session_log,
                   "report": self.report.json_report()}
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)
        return path
