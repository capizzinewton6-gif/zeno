"""Interactive visual graph of function call paths.

Generates Mermaid/Graphviz source for call graphs produced by the code graph
builder, and a plain-text fallback for terminal contexts.
"""
from __future__ import annotations

from typing import Any

from modeling.code_graph import CallGraph


class CallGraphPlotter:
    """Plots call graphs as Mermaid, DOT, or ASCII."""

    def to_mermaid(self, graph: CallGraph) -> str:
        lines = ["graph TD"]
        for edge in graph.edges:
            lines.append(f'    {self._id(edge.caller)}["{edge.caller}"] --> '
                         f'{self._id(edge.callee)}["{edge.callee}"]')
        # Isolated nodes
        for node in graph.nodes:
            if not any(e.caller == node or e.callee == node for e in graph.edges):
                lines.append(f'    {self._id(node)}["{node}"]')
        return "\n".join(lines)

    def to_dot(self, graph: CallGraph) -> str:
        lines = ["digraph callgraph {"]
        for edge in graph.edges:
            lines.append(f'    "{edge.caller}" -> "{edge.callee}";')
        lines.append("}")
        return "\n".join(lines)

    def to_ascii(self, graph: CallGraph) -> str:
        if not graph.edges:
            return "(no call edges)"
        lines: list[str] = []
        for edge in graph.edges:
            lines.append(f"{edge.caller} -> {edge.callee}")
        return "\n".join(lines)

    def impact_subgraph(self, graph: CallGraph, target: str) -> str:
        affected = graph.reverse_reachable(target)
        nodes = affected | {target}
        lines = [f"graph TD  # impact of {target}"]
        for edge in graph.edges:
            if edge.caller in nodes and edge.callee in nodes:
                lines.append(f'    {self._id(edge.caller)} --> {self._id(edge.callee)}')
        return "\n".join(lines)

    def _id(self, name: str) -> str:
        return name.replace("-", "_").replace(".", "_")
