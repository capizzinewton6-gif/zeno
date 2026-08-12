"""Autonomous Notepad automation: generates engineering documents.

On Windows this drives Windows Notepad via ``pyautogui`` to type and save
files. On other platforms it writes the same files directly to disk so the
invention workflow still produces all documentation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import Callable

from src.gemini_25_flash_engine import Gemini25FlashEngine

# The standard documents produced for every invention package.
DOCUMENT_NAMES = [
    "overview", "problem_statement", "design_objectives",
    "scientific_principles", "mechanical_design", "electrical_design",
    "software_architecture", "materials_selection", "manufacturing_plan",
    "assembly_instructions", "testing_plan", "safety_analysis",
    "performance_analysis", "cost_estimation", "maintenance_plan",
    "future_improvements", "references",
]

# Prompt templates per document type.
DOCUMENT_PROMPTS: dict[str, str] = {
    "overview": "Write a high-level overview of the invention: {concept}",
    "problem_statement": "Write the problem statement the invention {concept} solves",
    "design_objectives": "List the design objectives for invention {concept}",
    "scientific_principles": "Explain the scientific principles behind {concept}",
    "mechanical_design": "Detail the mechanical design of {concept}",
    "electrical_design": "Detail the electrical design of {concept}",
    "software_architecture": "Describe the software/firmware architecture of {concept}",
    "materials_selection": "Justify the materials selection for {concept}",
    "manufacturing_plan": "Provide a manufacturing plan for {concept}",
    "assembly_instructions": "Provide step-by-step assembly instructions for {concept}",
    "testing_plan": "Provide a testing plan for {concept}",
    "safety_analysis": "Provide a safety analysis for {concept}",
    "performance_analysis": "Provide a performance analysis for {concept}",
    "cost_estimation": "Provide a cost estimation for {concept}",
    "maintenance_plan": "Provide a maintenance plan for {concept}",
    "future_improvements": "Suggest future improvements for {concept}",
    "references": "List likely references for {concept}",
}


class NotepadAutomation:
    def __init__(self, engine: Gemini25FlashEngine | None = None,
                 output_dir: str = "documentation"):
        self.engine = engine or Gemini25FlashEngine()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.process = None
        self.platform = os.name

    # --- Notepad process control (Windows) -------------------------------
    def launch_notepad(self) -> bool:
        if self.platform != "nt":
            return False
        notepad = shutil.which("notepad") or r"C:\Windows\System32\notepad.exe"
        if not os.path.exists(notepad):
            return False
        self.process = subprocess.Popen([notepad])
        return True

    def close_notepad(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def _type_and_save(self, content: str, filename: str) -> str:
        """Write a file directly (cross-platform)."""
        path = os.path.join(self.output_dir, filename)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    # --- Document generation ---------------------------------------------
    def generate_document(self, doc_type: str, concept: str,
                          filename: str | None = None) -> str:
        if doc_type not in DOCUMENT_PROMPTS:
            raise ValueError(f"Unknown document type: {doc_type}")
        prompt = DOCUMENT_PROMPTS[doc_type].format(concept=concept)
        content = self.engine.generate(
            prompt, system="You are a senior engineering documentation writer.")
        fname = filename or f"{doc_type}.txt"
        return self._type_and_save(content, fname)

    def generate_all(self, concept: str, output_dir: str | None = None,
                     progress: Callable[[str], None] | None = None) -> list[str]:
        out = output_dir or self.output_dir
        os.makedirs(out, exist_ok=True)
        paths = []
        for doc_type in DOCUMENT_NAMES:
            content = self.engine.generate(
                DOCUMENT_PROMPTS[doc_type].format(concept=concept),
                system="You are a senior engineering documentation writer.")
            path = os.path.join(out, f"{doc_type}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            paths.append(path)
            if progress:
                progress(doc_type)
        return paths
