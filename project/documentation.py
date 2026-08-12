"""Generate LaTeX technical documentation and physical reports."""

from __future__ import annotations

import textwrap


class Documentation:
    """Render LaTeX technical reports."""

    @staticmethod
    def generate(title: str, body: str) -> str:
        return textwrap.dedent(f"""\
            \\documentclass{{article}}
            \\usepackage{{amsmath,amssymb,geometry}}
            \\geometry{{margin=1in}}
            \\title{{{title}}}
            \\date{{}}
            \\begin{{document}}
            \\maketitle
            {body}
            \\end{{document}}
            """)

    @staticmethod
    def section(name: str, content: str) -> str:
        return f"\\section{{{name}}}\n{content}\n"

    @staticmethod
    def equation(latex: str) -> str:
        return f"\\begin{{equation}}\n{latex}\n\\end{{equation}}\n"
