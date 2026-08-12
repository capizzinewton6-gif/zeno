"""Generate publication-ready biology papers."""
from __future__ import annotations

from datetime import datetime


class ReportGenerator:
    @staticmethod
    def lab_report(title: str, authors: list[str], abstract: str,
                   introduction: str, methods: str, results: str,
                   discussion: str, references: list[str] | None = None) -> str:
        ref_text = "\n".join(f"[{i+1}] {r}" for i, r in enumerate(references or []))
        return (
            f"# {title}\n\n"
            f"**Authors:** {', '.join(authors)}\n\n"
            f"**Date:** {datetime.utcnow().date().isoformat()}\n\n"
            f"## Abstract\n\n{abstract}\n\n"
            f"## 1. Introduction\n\n{introduction}\n\n"
            f"## 2. Methods\n\n{methods}\n\n"
            f"## 3. Results\n\n{results}\n\n"
            f"## 4. Discussion\n\n{discussion}\n\n"
            f"## References\n\n{ref_text}\n"
        )

    @staticmethod
    def research_paper(title: str, abstract: str, sections: dict,
                        references: list[str] | None = None) -> str:
        lines = [f"# {title}", "", "## Abstract", "", abstract, ""]
        for heading, content in sections.items():
            lines += [f"## {heading}", "", content, ""]
        if references:
            lines += ["## References", ""]
            lines += [f"[{i+1}] {r}" for i, r in enumerate(references)]
        return "\n".join(lines)

    @staticmethod
    def figure_caption(number: int, title: str, description: str) -> str:
        return f"**Figure {number}. {title}.** {description}\n"

    @staticmethod
    def table_caption(number: int, title: str, headers: list[str],
                      rows: list[list]) -> str:
        lines = [f"**Table {number}. {title}.**", "",
                 "| " + " | ".join(headers) + " |",
                 "| " + " | ".join("---" for _ in headers) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")
        return "\n".join(lines)
