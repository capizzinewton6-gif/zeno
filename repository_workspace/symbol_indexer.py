"""Universal symbol indexer for jump-to-definition mapping."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from modeling.ast_manager import ASTManager, Symbol
from repository_workspace.file_tree_indexer import FileTreeIndexer


@dataclass
class SymbolLocation:
    name: str
    kind: str
    file: str
    line: int
    end_line: int
    language: str


@dataclass
class SymbolIndex:
    symbols: dict[str, list[SymbolLocation]] = field(default_factory=dict)

    def lookup(self, name: str) -> list[SymbolLocation]:
        return self.symbols.get(name, [])

    def all_names(self) -> list[str]:
        return list(self.symbols.keys())


class SymbolIndexer:
    """Builds a universal symbol index for jump-to-definition."""

    INDEXABLE = {"python", "javascript", "typescript", "rust", "go", "cpp", "c", "java", "kotlin"}

    def __init__(self, ast: ASTManager | None = None,
                 tree_indexer: FileTreeIndexer | None = None) -> None:
        self.ast = ast or ASTManager()
        self.tree_indexer = tree_indexer or FileTreeIndexer()

    def build(self, root: str | Path) -> SymbolIndex:
        root_path = Path(root)
        idx = SymbolIndex()
        tree = self.tree_indexer.index(root_path)
        ext_to_lang = {
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".rs": "rust", ".go": "go", ".cpp": "cpp", ".c": "c",
            ".java": "java", ".kt": "kotlin",
        }
        for rel in tree.files:
            ext = Path(rel).suffix.lower()
            lang = ext_to_lang.get(ext)
            if not lang or lang not in self.INDEXABLE:
                continue
            fpath = root_path / rel
            try:
                source = fpath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            parsed = self.ast.parse(source, lang)
            for sym in parsed.symbols:
                loc = SymbolLocation(
                    name=sym.name, kind=sym.kind, file=rel,
                    line=sym.start_line, end_line=sym.end_line, language=lang,
                )
                idx.symbols.setdefault(sym.name, []).append(loc)
        return idx

    def find_definition(self, idx: SymbolIndex, name: str) -> SymbolLocation | None:
        locs = idx.lookup(name)
        return locs[0] if locs else None

    def find_references(self, idx: SymbolIndex, name: str,
                        root: str | Path) -> list[str]:
        """Greppy reference search across files."""
        root_path = Path(root)
        refs: list[str] = []
        for dirpath, _, filenames in os.walk(root_path):
            for fname in filenames:
                if Path(fname).suffix not in {".py", ".js", ".ts", ".rs", ".go",
                                              ".cpp", ".c", ".java", ".kt"}:
                    continue
                fpath = Path(dirpath) / fname
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for i, line in enumerate(content.splitlines(), 1):
                    if name in line:
                        refs.append(f"{fpath.relative_to(root_path)}:{i}")
        return refs
