"""Multi-file code generation and patch application.

Generates new files or patches existing ones, applying changes through the
safety layer. Supports full-file synthesis and unified-diff patch application.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ai_core.safety_layer import SafetyLayer
from modeling.neural_backbones import NeuralBackbone, get_backbone

SYNTHESIS_SYSTEM = (
    "You are a code synthesis engine. Produce clean, minimal, idiomatic code "
    "that matches the requested language and existing project style. Output "
    "only the file contents unless a patch format is requested."
)


@dataclass
class GeneratedFile:
    path: str
    content: str
    language: str = "python"
    overwrite: bool = False


@dataclass
class PatchResult:
    applied: bool
    path: str
    additions: int = 0
    deletions: int = 0
    error: str = ""


@dataclass
class SynthesisResult:
    files: list[GeneratedFile] = field(default_factory=list)
    patches: list[PatchResult] = field(default_factory=list)
    notes: str = ""


class CodeSynthesis:
    """Capability: generate and apply code across files."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 safety: SafetyLayer | None = None,
                 workspace: str = ".") -> None:
        self.backbone = backbone or get_backbone()
        self.safety = safety or SafetyLayer()
        self.workspace = workspace

    def generate(self, spec: str, language: str = "python",
                 filename: str | None = None) -> GeneratedFile:
        prompt = (
            f"# Specification\n{spec}\n\n# Language\n{language}\n\n"
            "Produce the complete file contents. Begin with ```language and end with ```."
        )
        resp = self.backbone.reason(prompt, system=SYNTHESIS_SYSTEM, task="synthesize")
        content = self._extract_block(resp.text) or resp.text
        return GeneratedFile(
            path=filename or f"generated.{language[:2]}",
            content=content, language=language,
        )

    def generate_multi(self, specs: list[dict[str, str]]) -> list[GeneratedFile]:
        return [self.generate(s["spec"], s.get("language", "python"), s.get("filename"))
                for s in specs]

    def write_file(self, file: GeneratedFile, overwrite: bool | None = None) -> PatchResult:
        target = Path(self.workspace) / file.path
        target.parent.mkdir(parents=True, exist_ok=True)
        decision = self.safety.check_write(str(target))
        if not decision:
            return PatchResult(False, str(target), error=decision.reason)

        exists = target.exists()
        if exists and not (overwrite if overwrite is not None else file.overwrite):
            return PatchResult(False, str(target),
                               error="File exists and overwrite not permitted.")

        old_lines = target.read_text(encoding="utf-8").splitlines() if exists else []
        target.write_text(file.content, encoding="utf-8")
        new_lines = file.content.splitlines()
        additions = max(0, len(new_lines) - len(old_lines))
        deletions = max(0, len(old_lines) - len(new_lines))
        return PatchResult(True, str(target), additions=additions, deletions=deletions)

    def apply_patch(self, path: str, patch: str) -> PatchResult:
        """Apply a simple unified-diff style patch to an existing file."""
        target = Path(self.workspace) / path
        if not target.exists():
            return PatchResult(False, str(target), error="Target file not found")
        decision = self.safety.check_write(str(target))
        if not decision:
            return PatchResult(False, str(target), error=decision.reason)

        original = target.read_text(encoding="utf-8").splitlines(keepends=True)
        patched, adds, dels, err = self._apply_unified(original, patch)
        if err:
            return PatchResult(False, str(target), error=err)
        target.write_text("".join(patched), encoding="utf-8")
        return PatchResult(True, str(target), additions=adds, deletions=dels)

    def _apply_unified(self, original: list[str], patch: str
                       ) -> tuple[list[str], int, int, str]:
        result = list(original)
        adds = dels = 0
        lines = patch.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^@@ -(\d+),?\d* \+(\d+),?\d* @@", line)
            if not m:
                i += 1
                continue
            start = int(m.group(1)) - 1
            i += 1
            idx = start
            while i < len(lines) and lines[i] and lines[i][0] in ("+", "-", " "):
                tag, content = lines[i][0], lines[i][1:]
                if tag == " ":
                    idx += 1
                elif tag == "-":
                    if idx < len(result) and result[idx].rstrip("\n") == content:
                        result.pop(idx)
                        dels += 1
                    else:
                        return result, adds, dels, f"Context mismatch at line {idx + 1}"
                elif tag == "+":
                    result.insert(idx, content + "\n")
                    idx += 1
                    adds += 1
                i += 1
        return result, adds, dels, ""

    def _extract_block(self, text: str) -> str | None:
        m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        return m.group(1) if m else None
