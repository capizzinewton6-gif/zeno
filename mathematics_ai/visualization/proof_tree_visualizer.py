"""Display formal proof graphs and dependency trees."""

from __future__ import annotations

from typing import Any


def build_proof_tree(steps: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a tree from a list of proof steps with dependencies.

    Each step: {"id": int, "statement": str, "rule": str, "depends_on": [int]}
    Returns {"nodes": [...], "edges": [...]}.
    """
    nodes = [{"id": s["id"], "statement": s.get("statement", ""), "rule": s.get("rule", "")} for s in steps]
    edges = []
    for s in steps:
        for dep in s.get("depends_on", []):
            edges.append({"from": dep, "to": s["id"]})
    return {"nodes": nodes, "edges": edges}


def to_ascii_tree(tree: dict[str, Any]) -> str:
    """Render a proof tree as ASCII art."""
    nodes = {n["id"]: n for n in tree["nodes"]}
    children: dict[int, list[int]] = {nid: [] for nid in nodes}
    for e in tree["edges"]:
        children[e["from"]].append(e["to"])
    roots = [nid for nid in nodes if not any(e["to"] == nid for e in tree["edges"])]
    lines = []
    for root in roots:
        _ascii_subtree(root, children, nodes, "", True, lines)
    return "\n".join(lines)


def _ascii_subtree(node_id, children, nodes, prefix, is_last, lines):
    node = nodes[node_id]
    connector = "└── " if is_last else "├── "
    lines.append(prefix + connector + f"[{node_id}] {node['statement'][:50]} ({node['rule']})")
    child_prefix = prefix + ("    " if is_last else "│   ")
    kids = children.get(node_id, [])
    for i, kid in enumerate(kids):
        _ascii_subtree(kid, children, nodes, child_prefix, i == len(kids) - 1, lines)


def proof_depth(tree: dict[str, Any], node_id: int) -> int:
    """Depth of a node from the roots."""
    parents = {e["to"]: e["from"] for e in tree["edges"]}
    depth = 0
    cur = node_id
    while cur in parents:
        cur = parents[cur]
        depth += 1
    return depth


def critical_path_length(tree: dict[str, Any]) -> int:
    """Length of the longest dependency chain."""
    nodes = {n["id"] for n in tree["nodes"]}
    parents = {e["to"]: e["from"] for e in tree["edges"]}
    if not nodes:
        return 0
    return max(proof_depth(tree, n) for n in nodes) + 1


__all__ = ["build_proof_tree", "to_ascii_tree", "proof_depth", "critical_path_length"]
