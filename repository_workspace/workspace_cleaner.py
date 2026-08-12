"""Caches, temporary file, and build artifact management."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer


@dataclass
class CleanResult:
    removed_dirs: list[str] = field(default_factory=list)
    removed_files: list[str] = field(default_factory=list)
    freed_bytes: int = 0
    skipped: list[str] = field(default_factory=list)


class WorkspaceCleaner:
    """Removes build artifacts, caches, and temp files."""

    ARTIFACT_DIRS = (
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "node_modules", "dist", "build", "target", ".next", ".nuxt",
        ".cache", "coverage", ".turbo", ".gradle", "out",
    )
    TEMP_PATTERNS = ("*.pyc", "*.pyo", "*.swp", "*.swo", "*.log", "*.tmp",
                     ".DS_Store", "Thumbs.db")

    def __init__(self, safety: SafetyLayer | None = None) -> None:
        self.safety = safety or SafetyLayer()

    def clean(self, root: str | Path, *, dry_run: bool = False) -> CleanResult:
        root_path = Path(root)
        result = CleanResult()
        for dirpath, dirnames, filenames in os.walk(root_path):
            for d in list(dirnames):
                if d in self.ARTIFACT_DIRS:
                    target = Path(dirpath) / d
                    size = self._dir_size(target)
                    decision = self.safety.check_delete(str(target))
                    if not decision:
                        result.skipped.append(str(target))
                        continue
                    if not dry_run:
                        shutil.rmtree(target, ignore_errors=True)
                    result.removed_dirs.append(str(target.relative_to(root_path)))
                    result.freed_bytes += size
            for f in filenames:
                if any(Path(f).match(p) for p in self.TEMP_PATTERNS):
                    target = Path(dirpath) / f
                    size = target.stat().st_size if target.exists() else 0
                    decision = self.safety.check_delete(str(target))
                    if not decision:
                        result.skipped.append(str(target))
                        continue
                    if not dry_run:
                        try:
                            target.unlink()
                        except OSError:
                            continue
                    result.removed_files.append(str(target.relative_to(root_path)))
                    result.freed_bytes += size
        return result

    def human_freed(self, result: CleanResult) -> str:
        from calculations.unit_converter import human_bytes
        return human_bytes(result.freed_bytes)

    def _dir_size(self, path: Path) -> int:
        total = 0
        if not path.exists():
            return 0
        for dirpath, _, files in os.walk(path):
            for f in files:
                fp = Path(dirpath) / f
                try:
                    total += fp.stat().st_size
                except OSError:
                    continue
        return total
