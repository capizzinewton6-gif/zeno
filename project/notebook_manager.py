"""Notebook manager: manage Jupyter notebooks for model training/evaluation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class Notebook:
    path: str
    title: str
    purpose: str = ""  # training | evaluation | exploration
    cells: int = 0
    tags: List[str] = field(default_factory=list)


class NotebookManager:
    """Create, list, and summarize Jupyter notebooks."""

    def __init__(self, base_dir: str = "notebooks") -> None:
        self.base_dir = base_dir

    def create(self, title: str, purpose: str = "exploration",
               cells: Optional[List[dict]] = None) -> Notebook:
        os.makedirs(self.base_dir, exist_ok=True)
        filename = title.lower().replace(" ", "_") + ".ipynb"
        path = os.path.join(self.base_dir, filename)
        nb = {
            "cells": cells or [
                {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
                {"cell_type": "code", "execution_count": None,
                 "metadata": {}, "outputs": [], "source": ["import cv2\nimport numpy as np\n"]},
            ],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
            "nbformat": 4, "nbformat_minor": 5,
        }
        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
        return Notebook(path=path, title=title, purpose=purpose, cells=len(nb["cells"]))

    def list(self) -> List[Notebook]:
        out = []
        if not os.path.isdir(self.base_dir):
            return out
        for name in os.listdir(self.base_dir):
            if not name.endswith(".ipynb"):
                continue
            path = os.path.join(self.base_dir, name)
            try:
                with open(path) as f:
                    nb = json.load(f)
                out.append(Notebook(path=path, title=name[:-6],
                                    cells=len(nb.get("cells", []))))
            except Exception:
                out.append(Notebook(path=path, title=name[:-6]))
        return out

    def cell_count(self, path: str) -> int:
        try:
            with open(path) as f:
                nb = json.load(f)
            return len(nb.get("cells", []))
        except Exception:
            return 0
