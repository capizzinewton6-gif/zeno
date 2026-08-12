"""File read/write operations and backup creation."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer


@dataclass
class FileOp:
    path: str
    ok: bool
    message: str = ""
    bytes: int = 0


@dataclass
class Backup:
    original: str
    backup_path: str
    ok: bool
    message: str = ""


class FileManager:
    """Safe file operations with backup support."""

    def __init__(self, safety: SafetyLayer | None = None) -> None:
        self.safety = safety or SafetyLayer()

    def read(self, path: str | Path) -> str | None:
        try:
            return Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    def write(self, path: str | Path, content: str,
              overwrite: bool = True) -> FileOp:
        p = Path(path)
        decision = self.safety.check_write(str(p))
        if not decision:
            return FileOp(str(p), False, decision.reason)
        if p.exists() and not overwrite:
            return FileOp(str(p), False, "file exists; overwrite=False")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return FileOp(str(p), True, "written", len(content.encode("utf-8")))

    def append(self, path: str | Path, content: str) -> FileOp:
        p = Path(path)
        decision = self.safety.check_write(str(p))
        if not decision:
            return FileOp(str(p), False, decision.reason)
        with open(p, "a", encoding="utf-8") as f:
            f.write(content)
        return FileOp(str(p), True, "appended")

    def delete(self, path: str | Path) -> FileOp:
        p = Path(path)
        decision = self.safety.check_delete(str(p))
        if not decision:
            return FileOp(str(p), False, decision.reason)
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return FileOp(str(p), True, "deleted")
        except OSError as exc:
            return FileOp(str(p), False, str(exc))

    def backup(self, path: str | Path, suffix: str = ".bak") -> Backup:
        p = Path(path)
        if not p.exists():
            return Backup(str(p), "", False, "source not found")
        dest = Path(str(p) + suffix)
        try:
            shutil.copy2(p, dest)
            return Backup(str(p), str(dest), True, "backed up")
        except OSError as exc:
            return Backup(str(p), str(dest), False, str(exc))

    def copy(self, src: str | Path, dest: str | Path) -> FileOp:
        s, d = Path(src), Path(dest)
        decision = self.safety.check_write(str(d))
        if not decision:
            return FileOp(str(d), False, decision.reason)
        try:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            return FileOp(str(d), True, "copied", s.stat().st_size)
        except OSError as exc:
            return FileOp(str(d), False, str(exc))

    def move(self, src: str | Path, dest: str | Path) -> FileOp:
        s, d = Path(src), Path(dest)
        decision = self.safety.check_write(str(d))
        if not decision:
            return FileOp(str(d), False, decision.reason)
        try:
            shutil.move(str(s), str(d))
            return FileOp(str(d), True, "moved")
        except OSError as exc:
            return FileOp(str(d), False, str(exc))
