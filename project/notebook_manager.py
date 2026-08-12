"""Jupyter Notebook execution and interactive cell management."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from capabilities.terminal_execution import TerminalExecution


@dataclass
class Cell:
    cell_type: str  # code, markdown, raw
    source: list[str] = field(default_factory=list)
    outputs: list[Any] = field(default_factory=list)
    execution_count: int | None = None


@dataclass
class Notebook:
    path: str
    cells: list[Cell] = field(default_factory=list)
    kernelspec: dict[str, str] = field(default_factory=lambda: {"name": "python3", "display_name": "Python 3"})

    def to_nbformat(self) -> dict[str, Any]:
        return {
            "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": self.kernelspec},
            "cells": [
                {
                    "cell_type": c.cell_type,
                    "source": c.source,
                    "outputs": c.outputs if c.cell_type == "code" else [],
                    "execution_count": c.execution_count if c.cell_type == "code" else None,
                    "metadata": {},
                }
                for c in self.cells
            ],
        }


class NotebookManager:
    """Create, edit, and execute Jupyter notebooks."""

    def __init__(self, terminal: TerminalExecution | None = None) -> None:
        self.terminal = terminal or TerminalExecution()

    def load(self, path: str | Path) -> Notebook:
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        cells = [Cell(cell_type=c.get("cell_type", "code"),
                      source=c.get("source", []),
                      outputs=c.get("outputs", []),
                      execution_count=c.get("execution_count"))
                 for c in data.get("cells", [])]
        ks = data.get("metadata", {}).get("kernelspec", {})
        return Notebook(path=str(p), cells=cells, kernelspec=ks)

    def save(self, notebook: Notebook) -> None:
        Path(notebook.path).write_text(
            json.dumps(notebook.to_nbformat(), indent=1), encoding="utf-8")

    def create(self, path: str | Path, cells: list[dict[str, str]] | None = None) -> Notebook:
        nb = Notebook(path=str(path))
        for c in cells or []:
            nb.cells.append(Cell(cell_type=c.get("type", "code"),
                                 source=c.get("source", "").splitlines(keepends=True)))
        self.save(nb)
        return nb

    def execute(self, path: str | Path) -> Any:
        """Execute a notebook in place using nbconvert if available."""
        return self.terminal.run(f"jupyter nbconvert --to notebook --execute --inplace {path}", timeout=300)

    def add_cell(self, notebook: Notebook, cell_type: str, source: str) -> None:
        notebook.cells.append(Cell(cell_type=cell_type,
                                   source=source.splitlines(keepends=True)))

    def clear_outputs(self, notebook: Notebook) -> None:
        for c in notebook.cells:
            if c.cell_type == "code":
                c.outputs = []
                c.execution_count = None
