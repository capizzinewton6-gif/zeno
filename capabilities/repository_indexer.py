"""Reads, trees, and indexes large code repositories.

Combines the repo mapper with the AST manager to produce a searchable index of
files, symbols, and call relationships. The index is cached to the memory
layer for reuse across sessions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config import load_json, memory_file, save_json
from modeling.ast_manager import ASTManager
from modeling.code_graph import CodeGraph
from modeling.repo_map import RepoFile, RepoMap, RepoMapper


@dataclass
class RepositoryIndex:
    root: str
    repo_map: RepoMap
    symbols: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    call_graph_edges: list[dict[str, Any]] = field(default_factory=list)
    imports: dict[str, list[str]] = field(default_factory=dict)
    indexed_files: int = 0

    def to_cache(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "languages": self.repo_map.languages,
            "total_files": self.repo_map.total_files,
            "total_lines": self.repo_map.total_lines,
            "symbols": self.symbols,
            "call_graph_edges": self.call_graph_edges,
            "imports": self.imports,
            "indexed_files": self.indexed_files,
        }


class RepositoryIndexer:
    """Capability: build and query a repository index."""

    def __init__(self, ast: ASTManager | None = None,
                 mapper: RepoMapper | None = None,
                 graph: CodeGraph | None = None) -> None:
        self.ast = ast or ASTManager()
        self.mapper = mapper or RepoMapper(self.ast)
        self.graph = graph or CodeGraph(self.ast)

    def index(self, root: str | Path, *, cache: bool = True) -> RepositoryIndex:
        root_path = Path(root)
        repo_map = self.mapper.map_directory(root_path)
        idx = RepositoryIndex(root=str(root_path), repo_map=repo_map)

        for rf in repo_map.files:
            lang = rf.language
            if lang not in {"python", "javascript", "typescript", "rust", "go", "cpp", "c", "java", "kotlin"}:
                continue
            path = root_path / rf.path
            try:
                source = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            parsed = self.ast.parse(source, lang)
            idx.symbols[rf.path] = [
                {"name": s.name, "kind": s.kind, "line": s.start_line,
                 "end": s.end_line, "signature": s.signature}
                for s in parsed.symbols
            ]
            if lang == "python":
                cg = self.graph.build(source, lang)
                for e in cg.edges:
                    idx.call_graph_edges.append(
                        {"caller": e.caller, "callee": e.callee, "file": rf.path})
                idx.imports[rf.path] = self.graph.imports_in(source)
            idx.indexed_files += 1

        if cache:
            self._save_cache(idx)
        return idx

    def search_symbols(self, idx: RepositoryIndex, query: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = query.lower()
        for path, syms in idx.symbols.items():
            for s in syms:
                if q in s["name"].lower():
                    out.append({"file": path, **s})
        return out

    def files_for_language(self, idx: RepositoryIndex, language: str) -> list[RepoFile]:
        return [f for f in idx.repo_map.files if f.language == language]

    def _save_cache(self, idx: RepositoryIndex) -> None:
        data = load_json(memory_file("codebase_index.json"))
        data["repository_map"] = {
            "root": idx.root,
            "languages": idx.repo_map.languages,
            "file_count": idx.repo_map.total_files,
            "line_count": idx.repo_map.total_lines,
        }
        data["symbol_locations"] = idx.symbols
        data["indexed_files"] = idx.indexed_files
        from datetime import datetime, timezone
        data["indexed_at"] = datetime.now(timezone.utc).isoformat()
        save_json(memory_file("codebase_index.json"), data)
