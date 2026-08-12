"""Generate publication-ready LaTeX papers (AMS style)."""

from __future__ import annotations

from typing import Any

from mathematics_ai.project.documentation import generate_document, theorem_environment


def generate_paper(
    title: str,
    authors: list[str],
    abstract: str,
    sections: list[dict[str, str]],
    theorems: list[dict[str, str]] | None = None,
    references: list[dict[str, str]] | None = None,
) -> str:
    """Generate a complete AMS-style paper.

    sections: list of {"heading": str, "content": str}
    theorems: list of {"name": str, "statement": str, "proof": str}
    references: list of {"key": str, "entry": str}
    """
    body = []
    # abstract
    body.append("\\begin{abstract}")
    body.append(abstract)
    body.append("\\end{abstract}\n")

    # sections
    for s in sections:
        body.append(f"\\section{{{s.get('heading', '')}}}")
        body.append(s.get("content", ""))
        if theorems:
            for t in theorems:
                body.append(theorem_environment(t.get("name", "theorem"), t["statement"], t.get("proof")))
        body.append("")

    doc = (
        "\\documentclass{amsart}\n"
        "\\usepackage{amsmath, amssymb, amsthm}\n"
        "\\newtheorem{theorem}{Theorem}[section]\n"
        "\\newtheorem{lemma}[theorem]{Lemma}\n"
        "\\newtheorem{proposition}[theorem]{Proposition}\n"
        "\\newtheorem{corollary}[theorem]{Corollary}\n"
        f"\\title{{{title}}}\n"
        "\\author{" + " \\and ".join(authors) + "}\n"
        "\\begin{document}\n"
        "\\maketitle\n"
        + "\n".join(body)
    )
    if references:
        doc += "\\begin{thebibliography}{99}\n"
        for r in references:
            doc += f"\\bibitem{{{r['key']}}} {r['entry']}\n"
        doc += "\\end{thebibliography}\n"
    doc += "\\end{document}\n"
    return doc


__all__ = ["generate_paper"]
