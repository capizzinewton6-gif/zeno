"""Research manager: manage CV projects and deployment configurations."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class Project:
    name: str
    description: str = ""
    cameras: List[str] = field(default_factory=list)
    models: Dict[str, str] = field(default_factory=dict)
    config: Dict = field(default_factory=dict)
    status: str = "planning"  # planning | active | archived


class ResearchManager:
    """Manage multiple vision projects and their deployment configs."""

    def __init__(self, store_path: str = "memory/projects.json") -> None:
        self.store_path = store_path
        self.projects: Dict[str, Project] = {}
        self.load()

    def create(self, name: str, description: str = "") -> Project:
        p = Project(name=name, description=description)
        self.projects[name] = p
        self.save()
        return p

    def add_camera(self, project: str, camera_id: str) -> None:
        if project in self.projects and camera_id not in self.projects[project].cameras:
            self.projects[project].cameras.append(camera_id)
            self.save()

    def set_model(self, project: str, task: str, model: str) -> None:
        if project in self.projects:
            self.projects[project].models[task] = model
            self.save()

    def list(self) -> List[Project]:
        return list(self.projects.values())

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.store_path) or ".", exist_ok=True)
        with open(self.store_path, "w") as f:
            json.dump({k: asdict(v) for k, v in self.projects.items()}, f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.store_path):
            return
        with open(self.store_path) as f:
            data = json.load(f)
        for k, v in data.items():
            self.projects[k] = Project(**v)
