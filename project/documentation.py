"""Automated project specification and manual generator."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from capabilities.documentation_builder import DocumentationBuilder
from modeling.neural_backbones import NeuralBackbone, get_backbone
from modeling.repo_map import RepoMapper


@dataclass
class Spec:
    title: str
    overview: str
    requirements: list[str] = field(default_factory=list)
    architecture: str = ""
    api: str = ""
    risks: list[str] = field(default_factory=list)


class Documentation:
    """Generates project specifications and manuals."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 doc_builder: DocumentationBuilder | None = None) -> None:
        self.backbone = backbone or get_backbone()
        self.doc_builder = doc_builder or DocumentationBuilder(self.backbone)

    def generate_spec(self, description: str, root: str | Path = ".") -> Spec:
        mapper = RepoMapper()
        repo_map = mapper.map_directory(root)
        prompt = (
            "Generate a project specification document from this description "
            "and repository map. Include: overview, requirements, architecture, "
            "API summary, risks. Return plain markdown.\n\n"
            f"# Description\n{description}\n\n# Repository\n{repo_map.to_skeleton()}"
        )
        resp = self.backbone.reason(prompt, task="document")
        return self._parse(resp.text, description)

    def generate_manual(self, root: str | Path = ".") -> str:
        return self.doc_builder.generate_readme(root).content

    def _parse(self, text: str, fallback: str) -> Spec:
        import re
        sections: dict[str, str] = {}
        current = "overview"
        buffer: list[str] = []
        for line in text.splitlines():
            m = re.match(r"^#+\s*(.+)$", line)
            if m:
                sections[current] = "\n".join(buffer).strip()
                current = m.group(1).strip().lower()
                buffer = []
            else:
                buffer.append(line)
        sections[current] = "\n".join(buffer).strip()
        return Spec(
            title=sections.get("title", fallback[:60]),
            overview=sections.get("overview", fallback),
            requirements=[l.lstrip("-*0123456789. )").strip()
                          for l in sections.get("requirements", "").splitlines() if l.strip()],
            architecture=sections.get("architecture", ""),
            api=sections.get("api", ""),
            risks=[l.lstrip("-*0123456789. )").strip()
                   for l in sections.get("risks", "").splitlines() if l.strip()],
        )
