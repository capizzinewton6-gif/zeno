"""
actions - file_controller
==========================
Create, move, copy and delete files.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from core.capability import Capability


class FileController(Capability):
    """Create, move, copy and delete files."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "file_controller"
        self.description = "Create, move, copy and delete files."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Parse a natural-language file task and execute it."""
        low = task.lower()
        try:
            if low.startswith(("list", "show files", "ls ", "list dir")):
                return self._list(task)
            if low.startswith("find file"):
                return self._find(task)
            if low.startswith(("create file", "write file", "make file")):
                return self._create(task)
            if low.startswith(("read file", "cat ", "show file")):
                return self._read(task)
            if low.startswith(("move file", "rename file")):
                return self._move(task)
            if low.startswith("copy file"):
                return self._copy(task)
            if low.startswith(("delete file", "remove file", "rm file")):
                return self._delete(task)
            if low.startswith("create dir") or low.startswith("mkdir"):
                return self._mkdir(task)
            return self.error(f"Unrecognised file task: {task}")
        except Exception as exc:
            return self.error(str(exc))

    # -- operations --------------------------------------------------------

    def _paths_after(self, task: str) -> list:
        return re.findall(r'["\']([^"\']+)["\']', task)

    def _list(self, task: str) -> Any:
        low = task.lower()
        # Strip leading "list" / "ls" / "show files" / "list dir" command word.
        for prefix in ("show files in", "show files", "list dir", "list files in", "list files", "list ", "ls "):
            if low.startswith(prefix):
                remainder = task[len(prefix):].strip()
                break
        else:
            remainder = task.strip()
        directory = remainder.strip("\"'") or "."
        path = Path(directory).expanduser()
        if not path.is_dir():
            return self.error(f"Not a directory: {path}")
        entries = sorted(p.name for p in path.iterdir())
        if not entries:
            return self.ok(f"(empty) {path}", count=0)
        listing = "\n".join(entries)
        return self.ok(f"{path} ({len(entries)} items):\n{listing}", count=len(entries))

    def _find(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if not quoted:
            return self.error("Specify a filename in quotes, e.g. find file \"notes.txt\"")
        target = quoted[0]
        roots = [Path(".").resolve()]
        for root in roots:
            for found in root.rglob(target):
                return self.ok(str(found), path=str(found))
        return self.error(f"File not found: {target}")

    def _create(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if not quoted:
            return self.error("Specify a path in quotes, e.g. create file \"path/to/file.txt\" \"content\"")
        path = Path(quoted[0]).expanduser()
        content = quoted[1] if len(quoted) > 1 else ""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return self.ok(f"Created {path} ({len(content)} bytes)", path=str(path))

    def _read(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if not quoted:
            return self.error("Specify a path in quotes, e.g. read file \"path/to/file.txt\"")
        path = Path(quoted[0]).expanduser()
        if not path.is_file():
            return self.error(f"Not a file: {path}")
        content = path.read_text(encoding="utf-8", errors="replace")
        if len(content) > 4000:
            content = content[:4000] + f"\n... ({len(content)} bytes total, truncated)"
        return self.ok(content, path=str(path))

    def _move(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if len(quoted) < 2:
            return self.error("Specify source and destination in quotes.")
        src, dst = Path(quoted[0]).expanduser(), Path(quoted[1]).expanduser()
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return self.ok(f"Moved {src} -> {dst}")

    def _copy(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if len(quoted) < 2:
            return self.error("Specify source and destination in quotes.")
        src, dst = Path(quoted[0]).expanduser(), Path(quoted[1]).expanduser()
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(str(src), str(dst))
        else:
            shutil.copy2(str(src), str(dst))
        return self.ok(f"Copied {src} -> {dst}")

    def _delete(self, task: str) -> Any:
        quoted = self._paths_after(task)
        if not quoted:
            return self.error("Specify a path in quotes.")
        path = Path(quoted[0]).expanduser()
        if not path.exists():
            return self.error(f"Not found: {path}")
        if path.is_dir():
            shutil.rmtree(str(path))
        else:
            path.unlink()
        return self.ok(f"Deleted {path}")

    def _mkdir(self, task: str) -> Any:
        quoted = self._paths_after(task)
        target = quoted[0] if quoted else task.split(maxsplit=1)[1] if len(task.split()) > 1 else ""
        if not target:
            return self.error("Specify a directory name.")
        path = Path(target).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return self.ok(f"Created directory {path}")
