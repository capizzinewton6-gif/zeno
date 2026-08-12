"""Generates system architecture diagrams (Mermaid / Graphviz)."""
from __future__ import annotations

from typing import Any


class ArchitectureRenderer:
    """Renders architecture blueprints as Mermaid/Graphviz diagrams."""

    def blueprint_to_mermaid(self, blueprint: dict[str, Any]) -> str:
        lines = ["graph TD"]
        for d in blueprint.get("directories", []):
            lines.append(f'    {self._id(d["path"])}["{d["path"]}<br/>{d.get("responsibility","")}"]')
        for i, iface in enumerate(blueprint.get("interfaces", [])):
            lines.append(f'    iface{i}(["{iface.get("name","iface")}"])')
        for step in blueprint.get("data_flow", []):
            lines.append(f'    flow["{step}"]')
        # Connect directories sequentially as a layering hint
        dirs = blueprint.get("directories", [])
        for a, b in zip(dirs, dirs[1:]):
            lines.append(f"    {self._id(a['path'])} -.-> {self._id(b['path'])}")
        return "\n".join(lines)

    def blueprint_to_dot(self, blueprint: dict[str, Any]) -> str:
        lines = ["digraph architecture {", "  rankdir=LR;"]
        for d in blueprint.get("directories", []):
            lines.append(f'  "{d["path"]}" [shape=box];')
        for iface in blueprint.get("interfaces", []):
            lines.append(f'  "{iface.get("name","iface")}" [shape=ellipse];')
        for a, b in zip(blueprint.get("directories", []),
                        blueprint.get("directories", [])[1:]):
            lines.append(f'  "{a["path"]}" -> "{b["path"]}";')
        lines.append("}")
        return "\n".join(lines)

    def sequence_diagram(self, steps: list[str], actors: list[str] | None = None) -> str:
        lines = ["sequenceDiagram"]
        actors = actors or ["Agent", "Capability", "Model"]
        for a in actors:
            lines.append(f"    participant {a}")
        for i, step in enumerate(steps):
            sender = actors[i % len(actors)]
            receiver = actors[(i + 1) % len(actors)]
            lines.append(f"    {sender}->>{receiver}: {step}")
        return "\n".join(lines)

    def _id(self, name: str) -> str:
        return name.replace("/", "_").replace("-", "_").replace(".", "_")
