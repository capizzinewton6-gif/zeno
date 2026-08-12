"""Documentation generator: API specs, architecture diagrams, system docs."""

from __future__ import annotations

import os
from typing import List

from tools.diagram_generator import DiagramGenerator


class Documentation:
    """Generate Markdown documentation for modules and pipelines."""

    @staticmethod
    def module_doc(name: str, description: str, functions: List[dict]) -> str:
        lines = [f"# {name}", "", description, "", "## Functions", ""]
        for fn in functions:
            lines.append(f"### `{fn['name']}({', '.join(fn.get('params', []))})`")
            lines.append("")
            lines.append(fn.get("doc", "_(no description)_"))
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def architecture_doc(title: str, stages: List[str], notes: str = "") -> str:
        flow = DiagramGenerator.flowchart(stages, title)
        return f"# Architecture: {title}\n\n```\n{flow}\n```\n\n{notes}\n"

    @staticmethod
    def write(path: str, content: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return path
