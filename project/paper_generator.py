"""Generate publication-ready LaTeX manuscripts (REVTeX / APS / IOP style)."""

from __future__ import annotations

import textwrap


class PaperGenerator:
    """Assemble a full physics manuscript in LaTeX."""

    @staticmethod
    def generate(title: str, abstract: str, sections: dict[str, str],
                 style: str = "revtex", authors: str = "Physics AI") -> str:
        doc_class = "revtex4-2" if style == "revtex" else "article"
        sec_body = "\n".join(f"\\section{{{name}}}\n{content}\n" for name, content in sections.items())
        return textwrap.dedent(f"""\
            \\documentclass[aps,prl,reprint]{{{doc_class}}}
            \\usepackage{{amsmath,amssymb,graphicx}}
            \\title{{{title}}}
            \\author{{{authors}}}
            \\begin{{abstract}}
            {abstract}
            \\end{{abstract}}
            \\begin{{document}}
            \\maketitle
            {sec_body}
            \\bibliographystyle{{apsrev4-1}}
            \\end{{document}}
            """)
