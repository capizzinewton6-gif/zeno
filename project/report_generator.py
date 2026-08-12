"""Engineering report generator."""

from __future__ import annotations

import os
from typing import Any

from src.gemini_25_flash_engine import Gemini25FlashEngine


class ReportGenerator:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def generate(self, project: str, sections: list[str] | None = None) -> str:
        secs = sections or ["Executive Summary", "Introduction", "Methodology",
                            "Design", "Analysis", "Results", "Discussion",
                            "Conclusion", "References"]
        secs_str = ", ".join(secs)
        return self.engine.generate(
            f"Generate a research-paper-quality engineering report for project: "
            f"{project}. Include sections: {secs_str}.",
            system="You are a senior engineering report writer.")

    def executive_summary(self, project: str) -> str:
        return self.engine.generate(
            f"Write an executive summary for: {project}.",
            system="You are an engineering executive.")

    def technical_brief(self, project: str) -> str:
        return self.engine.generate(
            f"Write a 1-page technical brief for: {project}.",
            system="You are a technical writer.")

    def save(self, content: str, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
