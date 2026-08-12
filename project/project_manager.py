"""Project manager: invents and tracks engineering projects."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List


class ProjectManager:
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        self.projects_file = os.path.join(memory_dir, "projects.json")
        os.makedirs(memory_dir, exist_ok=True)
        if not os.path.exists(self.projects_file):
            with open(self.projects_file, "w") as f:
                json.dump([], f)
        self.projects: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        with open(self.projects_file, encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(self.projects, f, indent=2)

    def create(self, name: str, description: str,
               discipline: str = "") -> Dict[str, Any]:
        project = {
            "id": f"proj_{int(time.time())}",
            "name": name, "description": description,
            "discipline": discipline,
            "status": "created", "created_at": time.time(),
            "tasks": [], "files": [],
        }
        self.projects.append(project)
        self._save()
        return project

    def get(self, project_id: str) -> Dict[str, Any] | None:
        for p in self.projects:
            if p["id"] == project_id:
                return p
        return None

    def list(self) -> List[Dict[str, Any]]:
        return list(self.projects)

    def update_status(self, project_id: str, status: str):
        p = self.get(project_id)
        if p:
            p["status"] = status
            self._save()

    def delete(self, project_id: str) -> bool:
        before = len(self.projects)
        self.projects = [p for p in self.projects if p["id"] != project_id]
        self._save()
        return len(self.projects) < before
