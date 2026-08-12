"""Read, parse and summarize mathematical research papers.

Lightweight: extracts text from local PDF/tex/txt files. Full PDF parsing
requires an external tool; this module degrades gracefully when unavailable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def read_paper(path: str) -> dict[str, Any]:
    """Read a paper file and extract raw text + sections heuristic."""
    p = Path(path)
    text = ""
    if p.suffix.lower() == ".tex":
        text = _strip_latex(p.read_text(encoding="utf-8", errors="ignore"))
    elif p.suffix.lower() == ".txt":
        text = p.read_text(encoding="utf-8", errors="ignore")
    elif p.suffix.lower() == ".pdf":
        text = _extract_pdf_text(p)
    else:
        text = p.read_text(encoding="utf-8", errors="ignore")
    return {
        "path": str(p.resolve()),
        "sections": _split_sections(text),
        "word_count": len(text.split()),
        "text": text[:5000],  # cap preview
    }


def summarize(path: str, max_sentences: int = 5) -> dict[str, Any]:
    """Extractive summary: first sentence of each section."""
    paper = read_paper(path)
    sentences: list[str] = []
    for section, body in paper["sections"].items():
        first = _first_sentence(body)
        if first:
            sentences.append(f"[{section}] {first}")
    return {"path": paper["path"], "summary": sentences[:max_sentences], "word_count": paper["word_count"]}


def _split_sections(text: str) -> dict[str, str]:
    """Heuristic: split on lines starting with 'Section', '\\section{}', or all-caps headers."""
    import re
    sections: dict[str, str] = {"_intro": ""}
    current = "_intro"
    for line in text.splitlines():
        m = re.match(r"\\section\{(.+?)\}", line) or re.match(r"^(\d+\.?\s+[A-Z].+)$", line)
        if m:
            current = m.group(1).strip()
            sections[current] = ""
        else:
            sections[current] = sections.get(current, "") + line + "\n"
    return sections


def _first_sentence(text: str) -> str:
    import re
    m = re.search(r"([^.!?]*[.!?])", text.strip())
    return m.group(1).strip() if m else text.strip()[:200]


def _strip_latex(tex: str) -> str:
    import re
    tex = re.sub(r"\\(begin|end)\{[^}]*\}", "", tex)
    tex = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})?", "", tex)
    tex = re.sub(r"[%].*", "", tex)
    tex = re.sub(r"\$[^$]*\$", "", tex)
    return tex


def _extract_pdf_text(path: Path) -> str:
    """Try pdfminer, fall back to empty string."""
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        return extract_text(str(path))
    except Exception:
        return f"[PDF parsing unavailable for {path.name}; install pdfminer.six]"


__all__ = ["read_paper", "summarize"]
