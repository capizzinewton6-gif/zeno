"""Generate LaTeX research documentation."""

from __future__ import annotations

from typing import Any


def generate_document(title: str, sections: list[dict[str, str]]) -> str:
    """Generate an AMS-style LaTeX document.

    sections: list of {"heading": str, "content": str}
    """
    body = []
    for s in sections:
        body.append(f"\\section{{{s.get('heading', '')}}}")
        body.append(s.get("content", ""))
        body.append("")
    return (
        "\\documentclass{amsart}\n"
        "\\usepackage{amsmath, amssymb, amsthm}\n"
        "\\newtheorem{theorem}{Theorem}\n"
        "\\newtheorem{lemma}[theorem]{Lemma}\n"
        "\\newtheorem{corollary}[theorem]{Corollary}\n"
        "\\title{" + title + "}\n"
        "\\begin{document}\n"
        "\\maketitle\n"
        + "\n".join(body) +
        "\\end{document}\n"
    )


def theorem_environment(name: str, statement: str, proof: str | None = None) -> str:
    out = f"\\begin{{{name}}}\n{statement}\n\\end{{{name}}}\n"
    if proof is not None:
        out += f"\\begin{{proof}}\n{proof}\n\\end{{proof}}\n"
    return out


def align_environment(lines: list[str]) -> str:
    body = " \\\\\n  ".join(lines)
    return f"\\begin{{align*}}\n  {body}\n\\end{{align*}}\n"


__all__ = ["generate_document", "theorem_environment", "align_environment"]
