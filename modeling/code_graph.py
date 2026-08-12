"""Symbol call graphs, dependency paths, and import tracking.

Builds a directed graph of which symbols call which, then answers reachability
and dependency questions useful for impact analysis and refactor planning.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from modeling.ast_manager import ASTManager


@dataclass
class CallEdge:
    caller: str
    callee: str
    line: int = 0
    file: str = ""


@dataclass
class CallGraph:
    nodes: set[str] = field(default_factory=set)
    edges: list[CallEdge] = field(default_factory=list)
    _adj: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def add_edge(self, caller: str, callee: str, line: int = 0, file: str = "") -> None:
        self.nodes.add(caller)
        self.nodes.add(callee)
        edge = CallEdge(caller=caller, callee=callee, line=line, file=file)
        self.edges.append(edge)
        self._adj[caller].add(callee)

    def callees_of(self, symbol: str) -> set[str]:
        return set(self._adj.get(symbol, set()))

    def callers_of(self, symbol: str) -> set[str]:
        return {e.caller for e in self.edges if e.callee == symbol}

    def reachable_from(self, start: str) -> set[str]:
        visited: set[str] = set()
        queue: deque[str] = deque([start])
        while queue:
            n = queue.popleft()
            for nxt in self._adj.get(n, set()):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return visited

    def reverse_reachable(self, target: str) -> set[str]:
        """Symbols that can transitively call ``target`` (impact set)."""
        rev = defaultdict(set)
        for e in self.edges:
            rev[e.callee].add(e.caller)
        visited: set[str] = set()
        queue: deque[str] = deque([target])
        while queue:
            n = queue.popleft()
            for prev in rev.get(n, set()):
                if prev not in visited:
                    visited.add(prev)
                    queue.append(prev)
        return visited

    def topological_order(self) -> list[str]:
        in_degree: dict[str, int] = {n: 0 for n in self.nodes}
        for e in self.edges:
            in_degree[e.callee] = in_degree.get(e.callee, 0) + 1
        queue = deque([n for n, d in in_degree.items() if d == 0])
        order: list[str] = []
        while queue:
            n = queue.popleft()
            order.append(n)
            for m in self._adj.get(n, set()):
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    queue.append(m)
        return order


class CodeGraph:
    """Builds a call graph from source code via the AST manager."""

    def __init__(self, ast_manager: ASTManager | None = None) -> None:
        self.ast = ast_manager or ASTManager()

    def build(self, source: str, language: str = "python") -> CallGraph:
        import ast as _ast

        graph = CallGraph()
        if language.lower() != "python":
            return graph
        try:
            tree = _ast.parse(source)
        except SyntaxError:
            return graph

        for node in _ast.walk(tree):
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
                for sub in _ast.walk(node):
                    if isinstance(sub, _ast.Call) and isinstance(sub.func, _ast.Name):
                        graph.add_edge(node.name, sub.func.id, line=node.lineno)
        return graph

    def dependency_path(self, graph: CallGraph, src: str, dst: str) -> list[str] | None:
        if src == dst:
            return [src]
        visited: set[str] = {src}
        queue: deque[tuple[str, list[str]]] = deque([(src, [src])])
        while queue:
            node, path = queue.popleft()
            for nxt in graph._adj.get(node, set()):
                if nxt == dst:
                    return path + [dst]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))
        return None

    def imports_in(self, source: str) -> list[str]:
        import ast as _ast

        try:
            tree = _ast.parse(source)
        except SyntaxError:
            return []
        out: list[str] = []
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                out.extend(a.name for a in node.names)
            elif isinstance(node, _ast.ImportFrom):
                mod = node.module or ""
                out.extend(f"{mod}.{a.name}" for a in node.names)
        return out
