"""CAD project manager: organizes CAD artifacts for an invention project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class CADProject:
    name: str
    directory: str
    views: List[str] = field(default_factory=list)
    drawings: List[str] = field(default_factory=list)
    models: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


class CADManager:
    def __init__(self, base_dir: str = "projects"):
        self.base_dir = base_dir

    def create_project(self, name: str) -> CADProject:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name) or "cad"
        directory = os.path.join(self.base_dir, safe, "blueprints")
        os.makedirs(directory, exist_ok=True)
        return CADProject(name=name, directory=directory)

    def register_view(self, project: CADProject, view_name: str, path: str):
        project.views.append(view_name)
        project.drawings.append(path)

    def register_model(self, project: CADProject, path: str):
        project.models.append(path)

    def list_artifacts(self, project: CADProject) -> List[str]:
        if not os.path.isdir(project.directory):
            return []
        return sorted(os.listdir(project.directory))
