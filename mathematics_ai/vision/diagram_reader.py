"""Parse geometric figures and commutative diagrams."""

from __future__ import annotations

import re
from typing import Any


def parse_tikz_diagram(tikz: str) -> dict[str, Any]:
    """Parse TikZ source into nodes and edges."""
    nodes = re.findall(r"\\node\s*(?:\[(.*?)\])?\s*(\w+)\s*(?:at\s*\((.*?)\))?\s*\{(.*?)\}\s*;", tikz)
    # also match "\\node (name) {label};" form (no identifier between node and label)
    if not nodes:
        nodes = re.findall(r"\\node\s*(?:\[(.*?)\])?\s*\((\w+)\)\s*(?:at\s*\((.*?)\))?\s*\{(.*?)\}\s*;", tikz)
    edges = re.findall(r"\\(?:draw|path)\s*(?:\[(.*?)\])?\s*\((\w+)\)\s*(--|->|<-)\s*\((\w+)\)", tikz)
    return {
        "nodes": [{"options": n[0], "name": n[1], "position": n[2], "label": n[3]} for n in nodes],
        "edges": [{"options": e[0], "from": e[1], "style": e[2], "to": e[3]} for e in edges],
    }


def extract_shapes_from_svg(svg: str) -> list[dict[str, str]]:
    """Extract basic shapes (circle, line, polygon) from SVG."""
    shapes = []
    circles = re.findall(r"<circle[^>]*cx=\"([^\"]+)\"[^>]*cy=\"([^\"]+)\"[^>]*r=\"([^\"]+)\"", svg)
    for c in circles:
        shapes.append({"type": "circle", "cx": c[0], "cy": c[1], "r": c[2]})
    lines = re.findall(r"<line[^>]*x1=\"([^\"]+)\"[^>]*y1=\"([^\"]+)\"[^>]*x2=\"([^\"]+)\"[^>]*y2=\"([^\"]+)\"", svg)
    for l in lines:
        shapes.append({"type": "line", "x1": l[0], "y1": l[1], "x2": l[2], "y2": l[3]})
    polygons = re.findall(r"<polygon[^>]*points=\"([^\"]+)\"", svg)
    for p in polygons:
        shapes.append({"type": "polygon", "points": p})
    return shapes


def classify_diagram(svg_or_tikz: str) -> str:
    """Heuristically classify a diagram."""
    s = svg_or_tikz.lower()
    if "tikz" in s:
        return "tikz"
    if "<svg" in s:
        return "svg"
    if "commutat" in s or "arrow" in s:
        return "commutative_diagram"
    if "triangle" in s or "circle" in s or "polygon" in s:
        return "geometric_figure"
    return "unknown"


__all__ = ["parse_tikz_diagram", "extract_shapes_from_svg", "classify_diagram"]
