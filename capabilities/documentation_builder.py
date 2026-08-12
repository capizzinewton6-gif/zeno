"""Auto-generates READMEs, OpenAPI specs, and inline docstrings.

Produces human-readable documentation from source code and structure, using
the reasoning model for prose and the AST manager for symbol extraction.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from modeling.ast_manager import ASTManager
from modeling.neural_backbones import NeuralBackbone, get_backbone
from modeling.repo_map import RepoMapper

DOC_SYSTEM = (
    "You are a technical documentation writer. Generate clear, concise "
    "documentation in the requested format (README markdown, OpenAPI YAML, or "
    "docstrings). Prefer plain English and active voice."
)


@dataclass
class Document:
    path: str
    content: str
    format: str  # markdown, yaml, rst, docstring


class DocumentationBuilder:
    """Capability: generate documentation artifacts."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 ast: ASTManager | None = None,
                 mapper: RepoMapper | None = None) -> None:
        self.backbone = backbone or get_backbone()
        self.ast = ast or ASTManager()
        self.mapper = mapper or RepoMapper(self.ast)

    def generate_readme(self, root: str | Path) -> Document:
        repo_map = self.mapper.map_directory(root)
        prompt = (
            "Generate a README.md for this repository. Include: project title, "
            "description, features, installation, usage, and structure sections.\n\n"
            f"# Repository map\n{repo_map.to_skeleton()}\n"
        )
        resp = self.backbone.reason(prompt, system=DOC_SYSTEM, task="document")
        return Document(path="README.md", content=self._strip_fence(resp.text), format="markdown")

    def generate_openapi(self, source: str, language: str = "python") -> Document:
        symbols = self.ast.parse(source, language).symbols
        sigs = "\n".join(f"- {s.signature}" for s in symbols if s.signature)
        prompt = (
            "Generate an OpenAPI 3.0 YAML spec in fenced ```yaml for the API "
            "described by these route handlers/functions. Include paths, methods, "
            "request/response schemas, and examples.\n\n"
            f"# Endpoints\n{sigs}\n\n# Source\n{source[:3000]}"
        )
        resp = self.backbone.reason(prompt, system=DOC_SYSTEM, task="document")
        yaml = self._extract_block(resp.text, "yaml") or resp.text
        return Document(path="openapi.yaml", content=yaml, format="yaml")

    def generate_docstrings(self, source: str, language: str = "python") -> str:
        parsed = self.ast.parse(source, language)
        targets = [s for s in parsed.symbols if s.kind in ("function", "class") and not s.docstring]
        if not targets:
            return source
        names = ", ".join(s.name for s in targets)
        prompt = (
            f"Add concise Google-style docstrings to these functions/classes: {names}.\n"
            "Return the FULL source with docstrings inserted. No other commentary.\n\n"
            f"{source}"
        )
        resp = self.backbone.reason(prompt, system=DOC_SYSTEM, task="document")
        return self._strip_fence(resp.text) or source

    def _extract_block(self, text: str, lang: str | None = None) -> str | None:
        pattern = r"```(?:\w+)?\n(.*?)```" if lang is None else rf"```{lang}\n(.*?)```"
        m = re.search(pattern, text, re.DOTALL)
        return m.group(1) if m else None

    def _strip_fence(self, text: str) -> str:
        m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        return m.group(1) if m else text
