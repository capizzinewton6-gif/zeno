"""Auto-generates initial folder structure and boilerplate code."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer
from project_engine.project_templates import ProjectTemplate, ProjectTemplates


@dataclass
class ScaffoldingResult:
    project_name: str
    template: str
    created_files: list[str] = field(default_factory=list)
    root: str = ""


class ProjectScaffolder:
    """Materializes a project template onto disk."""

    def __init__(self, safety: SafetyLayer | None = None,
                 templates: ProjectTemplates | None = None) -> None:
        self.safety = safety or SafetyLayer()
        self.templates = templates or ProjectTemplates()

    def scaffold(self, template_name: str, project_name: str,
                 parent_dir: str = ".") -> ScaffoldingResult:
        template = self.templates.get(template_name)
        if not template:
            available = ", ".join(self.templates.list())
            raise ValueError(f"Unknown template '{template_name}'. Available: {available}")

        root = Path(parent_dir) / project_name
        created: list[str] = []
        for rel_path, content in template.files.items():
            target = root / rel_path
            decision = self.safety.check_write(str(target))
            if not decision:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            created.append(str(target.relative_to(parent_dir)))

        # Create a requirements/dependency file if not present
        if template.dependencies and not any("requirements" in f for f in created):
            req_path = root / "requirements.txt"
            req_path.write_text("\n".join(template.dependencies) + "\n", encoding="utf-8")
            created.append("requirements.txt")

        return ScaffoldingResult(project_name=project_name,
                                 template=template_name,
                                 created_files=created, root=str(root))

    def list_templates(self) -> list[str]:
        return self.templates.list()
