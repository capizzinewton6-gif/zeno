"""Track Jupyter, SageMath and Mathematica notebooks."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Notebook:
    name: str
    path: str
    kernel: str = "python3"  # "python3" | "sagemath" | "wolfram"
    cells: int = 0
    last_run: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class NotebookManager:
    """Registry of external notebooks associated with a project."""

    def __init__(self) -> None:
        self._notebooks: dict[str, Notebook] = {}

    def register(self, name: str, path: str, kernel: str = "python3") -> Notebook:
        nb = Notebook(name=name, path=path, kernel=kernel)
        self._notebooks[name] = nb
        return nb

    def get(self, name: str) -> Notebook | None:
        return self._notebooks.get(name)

    def list_notebooks(self) -> list[Notebook]:
        return list(self._notebooks.values())

    def count_cells(self, name: str) -> int | None:
        nb = self.get(name)
        if nb is None:
            return None
        try:
            import json
            from pathlib import Path
            data = json.loads(Path(nb.path).read_text())
            nb.cells = len(data.get("cells", []))
            return nb.cells
        except Exception:
            return nb.cells

    def run(self, name: str) -> dict[str, Any]:
        """Run a notebook via jupyter nbconvert (placeholder)."""
        nb = self.get(name)
        if nb is None:
            return {"ok": False, "error": "notebook not found"}
        import subprocess
        try:
            proc = subprocess.run(
                ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", nb.path],
                capture_output=True, text=True, timeout=300,
            )
            nb.last_run = time.time()
            return {"ok": proc.returncode == 0, "output": proc.stdout + proc.stderr}
        except Exception as e:
            return {"ok": False, "error": str(e)}


__all__ = ["Notebook", "NotebookManager"]
