"""Repository mapping and code skeletonization.

Walks a directory tree (respecting .gitignore) and produces a compact map of
files, languages, and skeletonized definitions suitable for LLM context.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config import get_settings

# Common binary/asset extensions to skip
_SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".pdf",
    ".zip", ".gz", ".tar", ".tgz", ".bz2", ".7z", ".rar", ".jar", ".war",
    ".class", ".pyc", ".pyo", ".o", ".so", ".dll", ".exe", ".bin",
    ".mp3", ".mp4", ".avi", ".mov", ".wav", ".woff", ".woff2", ".ttf",
    ".eot", ".lock", ".ds_store", ".db", ".sqlite",
}

_LANG_BY_EXT = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript",
    ".ts": "typescript", ".tsx": "typescript", ".rs": "rust", ".go": "go",
    ".c": "c", ".h": "c", ".cpp": "cpp", ".cc": "cpp", ".hpp": "cpp",
    ".java": "java", ".kt": "kotlin", ".kts": "kotlin",
    ".html": "html", ".htm": "html", ".css": "css", ".scss": "css",
    ".sql": "sql", ".sh": "bash", ".bash": "bash", ".ps1": "powershell",
    ".rb": "ruby", ".php": "php", ".swift": "swift", ".md": "markdown",
    ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
    ".xml": "xml",
}


@dataclass
class RepoFile:
    path: str
    language: str
    size: int
    lines: int


@dataclass
class RepoMap:
    root: str
    files: list[RepoFile] = field(default_factory=list)
    languages: dict[str, int] = field(default_factory=lambda: {})
    total_files: int = 0
    total_lines: int = 0

    def to_skeleton(self, max_files: int = 200) -> str:
        """Compact text skeleton of the repo for context injection."""
        lines = [f"# Repository map: {self.root}"]
        lines.append(f"# {self.total_files} files, {self.total_lines} lines")
        lines.append(f"# Languages: {dict(self.languages)}")
        lines.append("")
        for f in self.files[:max_files]:
            lines.append(f"- {f.path} [{f.language}] ({f.lines}L)")
        if len(self.files) > max_files:
            lines.append(f"... and {len(self.files) - max_files} more files")
        return "\n".join(lines)


class RepoMapper:
    """Builds a RepoMap for a given directory."""

    def __init__(self, ast_manager: Any = None) -> None:
        self.ast = ast_manager
        self._max_files = get_settings().get("repository", {}).get("max_indexed_files", 5000)
        self._ignore_dot = get_settings().get("repository", {}).get("ignore_dot_dirs", True)

    def map_directory(self, root: str | Path) -> RepoMap:
        root_path = Path(root)
        repo_map = RepoMap(root=str(root_path))
        gitignore = self._load_gitignore(root_path)
        count = 0

        for dirpath, dirnames, filenames in os.walk(root_path):
            if count >= self._max_files:
                break
            dirnames[:] = self._filter_dirs(dirnames, root_path, dirpath, gitignore)
            for fname in sorted(filenames):
                fpath = Path(dirpath) / fname
                rel = str(fpath.relative_to(root_path))
                if self._is_ignored(rel, gitignore):
                    continue
                ext = fpath.suffix.lower()
                if ext in _SKIP_EXT:
                    continue
                language = _LANG_BY_EXT.get(ext, "text")
                try:
                    size = fpath.stat().st_size
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        nlines = sum(1 for _ in f)
                except OSError:
                    continue
                repo_map.files.append(RepoFile(rel, language, size, nlines))
                repo_map.languages[language] = repo_map.languages.get(language, 0) + 1
                repo_map.total_lines += nlines
                count += 1
                if count >= self._max_files:
                    break

        repo_map.total_files = len(repo_map.files)
        return repo_map

    def _filter_dirs(self, dirs: list[str], root: Path, dirpath: str, gi: set[str]) -> list[str]:
        out = []
        for d in dirs:
            if self._ignore_dot and d.startswith("."):
                # allow top-level .agents-like dirs? keep skipping dot dirs.
                continue
            out.append(d)
        return out

    def _load_gitignore(self, root: Path) -> set[str]:
        gi = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
              "build", "target", ".next", ".nuxt", ".cache", "coverage"}
        gi_file = root / ".gitignore"
        if gi_file.exists():
            try:
                with open(gi_file, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            gi.add(line.rstrip("/"))
            except OSError:
                pass
        return gi

    def _is_ignored(self, rel: str, patterns: set[str]) -> bool:
        parts = Path(rel).parts
        return any(p in patterns for p in parts)
