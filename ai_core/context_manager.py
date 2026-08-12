"""Project context manager: maintains structured state for an invention
project across modules and stages."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class ProjectContext:
    name: str = ""
    problem_statement: str = ""
    objectives: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)
    mechanical_design: str = ""
    electrical_design: str = ""
    software_architecture: str = ""
    materials: List[Dict[str, Any]] = field(default_factory=list)
    calculations: Dict[str, Any] = field(default_factory=dict)
    bom: List[Dict[str, Any]] = field(default_factory=list)
    blueprints: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    testing_plan: str = ""
    manufacturing_plan: str = ""
    safety_analysis: str = ""
    cost_estimate: str = ""
    references: List[str] = field(default_factory=list)
    project_dir: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ProjectContext":
        return cls(**{k: d.get(k) for k in cls.__dataclass_fields__})


class ContextManager:
    """Holds the active project context and persists it to disk."""

    def __init__(self):
        self._context: ProjectContext | None = None

    @property
    def context(self) -> ProjectContext:
        if self._context is None:
            self._context = ProjectContext()
        return self._context

    def new_project(self, name: str, base_dir: str = "projects") -> ProjectContext:
        ctx = ProjectContext(name=name)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name) or "invention"
        ctx.project_dir = os.path.join(base_dir, safe)
        os.makedirs(ctx.project_dir, exist_ok=True)
        self._context = ctx
        return ctx

    def save(self) -> str:
        ctx = self.context
        if not ctx.project_dir:
            return ""
        path = os.path.join(ctx.project_dir, "context.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(ctx.to_json())
        return path

    def load(self, path: str) -> ProjectContext:
        with open(path, encoding="utf-8") as f:
            self._context = ProjectContext.from_dict(json.load(f))
        return self._context


context_manager = ContextManager()
