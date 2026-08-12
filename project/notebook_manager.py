"""Interface with Jupyter, Mathematica (.nb), and ROOT notebooks."""

from __future__ import annotations

import json
import os
from typing import Any


class NotebookManager:
    """Create and round-trip Jupyter notebooks; export to Python."""

    @staticmethod
    def new_notebook(cells: list[dict] | None = None) -> dict:
        return {
            "cells": cells or [],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
            "nbformat": 4,
            "nbformat_minor": 5,
        }

    @staticmethod
    def add_code_cell(nb: dict, source: str) -> dict:
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [source],
        })
        return nb

    @staticmethod
    def add_markdown_cell(nb: dict, source: str) -> dict:
        nb["cells"].append({"cell_type": "markdown", "metadata": {}, "source": [source]})
        return nb

    @staticmethod
    def save(nb: dict, path: str) -> str:
        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
        return path

    @staticmethod
    def load(path: str) -> dict:
        with open(path) as f:
            return json.load(f)

    @staticmethod
    def export_python(nb: dict) -> str:
        lines = []
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "code":
                lines.append("".join(cell["source"]))
                lines.append("")
        return "\n".join(lines)
