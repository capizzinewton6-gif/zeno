"""Flowchart and UML sequence diagram renderer."""
from __future__ import annotations

from typing import Any


class DiagramGenerator:
    """Generates Mermaid flowcharts and UML sequence diagrams."""

    def flowchart(self, steps: list[dict[str, str]],
                  direction: str = "TD") -> str:
        """Each step: {id, label, next (id or list)}."""
        lines = [f"graph {direction}"]
        for step in steps:
            sid = step.get("id", "")
            label = step.get("label", sid)
            shape = step.get("shape", "[]")
            lines.append(f'    {sid}{shape[0]}"{label}"{shape[1] if len(shape) > 1 else ""}')
        for step in steps:
            sid = step.get("id", "")
            nxt = step.get("next")
            if not nxt:
                continue
            if isinstance(nxt, str):
                nxt = [nxt]
            for n in nxt:
                lines.append(f"    {sid} --> {n}")
        return "\n".join(lines)

    def sequence(self, actors: list[str], messages: list[dict[str, str]]) -> str:
        """Each message: {from, to, text, type (sync|async|reply)}."""
        lines = ["sequenceDiagram"]
        for a in actors:
            lines.append(f"    participant {a}")
        for m in messages:
            arrow = "->>" if m.get("type", "sync") == "sync" else "-->>"
            if m.get("type") == "async":
                arrow = "-)"
            lines.append(f"    {m['from']} {arrow} {m['to']}: {m['text']}")
        return "\n".join(lines)

    def class_diagram(self, classes: list[dict[str, Any]]) -> str:
        lines = ["classDiagram"]
        for cls in classes:
            name = cls.get("name", "")
            lines.append(f"    class {name} {{")
            for attr in cls.get("attributes", []):
                lines.append(f"        +{attr}")
            for method in cls.get("methods", []):
                lines.append(f"        +{method}")
            lines.append("    }")
        for cls in classes:
            for parent in cls.get("extends", []):
                lines.append(f"    {parent} <|-- {cls['name']}")
        return "\n".join(lines)

    def state_diagram(self, states: list[dict[str, str]]) -> str:
        lines = ["stateDiagram-v2"]
        for s in states:
            if s.get("from") and s.get("to"):
                lines.append(f"    {s['from']} --> {s['to']}: {s.get('label', '')}")
            elif s.get("name"):
                lines.append(f"    {s['name']}")
        return "\n".join(lines)
