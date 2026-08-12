"""Documentation generator."""

from __future__ import annotations

import os
from typing import Any

from src.gemini_25_flash_engine import Gemini25FlashEngine


class Documentation:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def generate(self, doc_type: str, project: str) -> str:
        return self.engine.generate(
            f"Write a {doc_type} document for project: {project}. "
            f"Use clear engineering language.",
            system="You are a technical documentation engineer.")

    def overview(self, project: str) -> str:
        return self.generate("overview", project)

    def requirements_doc(self, project: str) -> str:
        return self.generate("requirements specification", project)

    def design_rationale(self, project: str) -> str:
        return self.generate("design rationale", project)

    def test_plan(self, project: str) -> str:
        return self.generate("test plan", project)

    def user_manual(self, project: str) -> str:
        return self.generate("user manual", project)

    def save(self, content: str, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
