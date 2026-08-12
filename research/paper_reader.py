"""Extracts insights from program synthesis research papers."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from modeling.neural_backbones import NeuralBackbone, get_backbone


@dataclass
class PaperInsight:
    title: str
    summary: str
    key_findings: list[str] = field(default_factory=list)
    techniques: list[str] = field(default_factory=list)
    relevance: str = ""


class PaperReader:
    """Summarizes research papers into actionable insights."""

    def __init__(self, backbone: NeuralBackbone | None = None) -> None:
        self.backbone = backbone or get_backbone()

    def read(self, text: str) -> PaperInsight:
        # Extract a candidate title (first non-empty line)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = lines[0][:120] if lines else "Untitled"
        prompt = (
            "Extract insights from this research paper text. Provide:\n"
            "1. A 2-sentence summary.\n"
            "2. Key findings (bulleted).\n"
            "3. Techniques proposed (bulleted).\n"
            "4. Relevance to AI code synthesis.\n\n"
            f"# Paper\n{text[:8000]}"
        )
        resp = self.backbone.reason(prompt, task="research")
        return self._parse(resp.text, title)

    def read_abstract(self, text: str) -> PaperInsight:
        m = re.search(r"(?i)abstract[:\s]*(.*?)(?:\n\s*\n|introduction|keywords|\Z)",
                      text, re.DOTALL)
        abstract = m.group(1).strip() if m else text[:1000]
        return self.read(abstract)

    def _parse(self, text: str, title: str) -> PaperInsight:
        sections = re.split(r"\n(?=[A-Z][\w ]+:)", text)
        summary = sections[0].strip()[:300]
        findings: list[str] = []
        techniques: list[str] = []
        relevance = ""
        for sec in sections[1:]:
            lower = sec.lower()
            if lower.startswith("key findings"):
                findings = [l.lstrip("-*0123456789. )").strip()
                            for l in sec.splitlines()[1:] if l.strip()]
            elif lower.startswith("techniques"):
                techniques = [l.lstrip("-*0123456789. )").strip()
                              for l in sec.splitlines()[1:] if l.strip()]
            elif lower.startswith("relevance"):
                relevance = "\n".join(sec.splitlines()[1:]).strip()
        return PaperInsight(title=title, summary=summary,
                            key_findings=findings, techniques=techniques,
                            relevance=relevance)
