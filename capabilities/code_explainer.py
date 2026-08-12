"""Translates complex logic and algorithms into step-by-step prose.

Uses the reasoning model to produce clear explanations of code, suitable for
teaching or onboarding. Falls back to structural analysis when offline.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from modeling.ast_manager import ASTManager
from modeling.neural_backbones import NeuralBackbone, get_backbone

EXPLAIN_SYSTEM = (
    "You are a code educator. Explain code as clear, numbered, step-by-step "
    "prose for a developer unfamiliar with this codebase. Define jargon, "
    "explain the 'why', and end with a one-sentence summary."
)


@dataclass
class Explanation:
    summary: str
    steps: list[str]
    raw: str
    symbols: list[str]


class CodeExplainer:
    """Capability: explain arbitrary source code."""

    def __init__(self, backbone: NeuralBackbone | None = None,
                 ast: ASTManager | None = None) -> None:
        self.backbone = backbone or get_backbone()
        self.ast = ast or ASTManager()

    def explain(self, source: str, language: str = "python",
                audience: str = "junior developer") -> Explanation:
        parsed = self.ast.parse(source, language)
        symbols = [s.name for s in parsed.symbols]
        prompt = (
            f"Explain the following {language} code for a {audience}.\n\n"
            f"# Symbols detected\n{', '.join(symbols) or 'none'}\n\n"
            f"# Code\n{source}\n\n"
            "Provide: a one-sentence summary, then numbered steps, then a final summary."
        )
        resp = self.backbone.reason(prompt, system=EXPLAIN_SYSTEM, task="explain")
        summary, steps = self._parse(resp.text)
        return Explanation(summary=summary, steps=steps, raw=resp.text, symbols=symbols)

    def explain_symbol(self, source: str, name: str, language: str = "python") -> Explanation:
        body = self.ast.extract_function(source, name, language) or source
        return self.explain(body, language)

    def _parse(self, text: str) -> tuple[str, list[str]]:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        summary = next(iter(lines), "")
        steps = [l.lstrip("0123456789.-) ").strip() for l in lines
                 if l and (l[0].isdigit() or l.startswith("- "))]
        if not steps:
            steps = lines[1:6]
        return summary, steps
