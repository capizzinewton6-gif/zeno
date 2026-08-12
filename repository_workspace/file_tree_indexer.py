"""Workspace file indexing with .gitignore handling."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


@dataclass
class FileIndex:
    root: str
    files: list[str] = field(default_factory=list)
    by_extension: dict[str, list[str]] = field(default_factory=dict)
    ignored: list[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.files)


class FileTreeIndexer:
    """Indexes a workspace tree, honoring .gitignore patterns."""

    DEFAULT_IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv",
                      "dist", "build", "target", ".cache"}

    def __init__(self, max_files: int = 5000) -> None:
        self.max_files = max_files

    def index(self, root: str | Path) -> FileIndex:
        root_path = Path(root)
        idx = FileIndex(root=str(root_path))
        patterns = self._load_gitignore(root_path)
        count = 0
        for dirpath, dirnames, filenames in os.walk(root_path):
            if count >= self.max_files:
                break
            dirnames[:] = [d for d in dirnames if d not in self.DEFAULT_IGNORE
                           and not self._ignored(d, patterns)]
            for fname in sorted(filenames):
                rel = str(Path(dirpath).relative_to(root_path) / fname)
                if self._ignored(rel, patterns):
                    idx.ignored.append(rel)
                    continue
                ext = Path(fname).suffix.lower() or "noext"
                idx.files.append(rel)
                idx.by_extension.setdefault(ext, []).append(rel)
                count += 1
                if count >= self.max_files:
                    break
        return idx

    def search(self, idx: FileIndex, query: str) -> list[str]:
        q = query.lower()
        return [f for f in idx.files if q in f.lower()]

    def _load_gitignore(self, root: Path) -> list[str]:
        patterns = list(self.DEFAULT_IGNORE)
        gi = root / ".gitignore"
        if gi.exists():
            try:
                with open(gi, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            patterns.append(line.rstrip("/"))
            except OSError:
                pass
        return patterns

    def _ignored(self, path: str, patterns: list[str]) -> bool:
        name = Path(path).name
        return any(fnmatch(name, p) or fnmatch(path, p) for p in patterns)
